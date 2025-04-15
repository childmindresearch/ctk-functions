"""Utility data fetching functions for all tables."""

import dataclasses
import functools
import statistics
from typing import Literal, TypeVar

import cmi_docx
import fastapi
import sqlalchemy
from starlette import status

from ctk_functions.core.config import get_logger
from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base

logger = get_logger()

T = TypeVar("T", bound=models.Base)


@dataclasses.dataclass
class UniqueIdentifiers:
    """Dataclass for the variety of unique identifiers used in HBN."""

    MRN: str
    EID: str
    person_id: str


def add_thick_top_border(
    markup: base.WordTableMarkup, row_index: int
) -> base.WordTableMarkup:
    """Convenience function for adding a thicker top borderline within a table.

    Args:
        markup: The Word table markup.
        row_index: The row index above which a thicker border will be added.

    Returns:
        New markup with a thicker top borderline added.
    """
    thick_top_border = base.ConditionalStyle(
        style=cmi_docx.CellStyle(
            borders=[
                cmi_docx.CellBorder(
                    sides=("top",),
                    sz=16,  # 2pt
                )
            ]
        )
    )
    for cell in markup.rows[row_index]:
        cell.formatter.conditional_styles.append(thick_top_border)
    return markup


@functools.lru_cache
def mrn_to_ids(mrn: str) -> UniqueIdentifiers:
    """Fetches a participant's EID from their MRN.

    EID (also known as GUID) and MRN are separate unique identifiers used
    in the NextGen database.

    Args:
        mrn: The MRN of the participant.

    Returns:
        The EID of the participant.
    """
    logger.debug("Fetching participant %s.", mrn)
    with client.get_session() as session:
        participant = session.execute(
            sqlalchemy.select(models.CmiHbnIdTrack).where(
                models.CmiHbnIdTrack.MRN == mrn,
            ),
        ).scalar_one_or_none()

    if not participant:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MRN {mrn} could not be converted to EID.",
        )

    logger.debug("Fetched participant %s.", mrn)
    return UniqueIdentifiers(
        MRN=mrn,
        EID=participant.GUID,
        person_id=participant.person_id,
    )


@functools.lru_cache
def fetch_participant_row(
    id_property: Literal["person_id", "EID", "MRN"],
    mrn: str,
    table: type[T],
) -> T:
    """Fetches a participant's row in the given table.

    The table must have an EID, person_id, or mrn property.

    Args:
        id_property: The identifier to use to select the row from the table.
        mrn: The participant's unique identifier.
        table: The table to fetch the row from.

    Returns:
        The participant's row in the given table.
    """
    logger.debug("Fetching table %s, participant %s.", table.__name__, mrn)
    identifier = getattr(mrn_to_ids(mrn), id_property)
    statement = sqlalchemy.select(table).where(
        getattr(table, id_property) == identifier,
    )

    with client.get_session() as session:
        data = session.execute(statement).scalar_one_or_none()

    logger.debug("Fetched table %s, participant %s,", table.__name__, mrn)
    if data:
        return data

    msg = f"Table data not found for {mrn}."
    raise base.TableDataNotFoundError(msg)


def standard_score_to_qualifier(score: float) -> str:  # noqa: PLR0911
    """Converts standard score to a qualifier.

    This was built with a mean of 100, and std of 15 as the underlying
    normal distribution.

    Args:
        score: The standard score to convert.

    Returns:
        The corresponding qualifier.
    """
    if score <= 59:  # noqa: PLR2004
        return "extremely low"
    if score <= 69:  # noqa: PLR2004
        return "very low"
    if score <= 79:  # noqa: PLR2004
        return "low"
    if score <= 89:  # noqa: PLR2004
        return "low average"
    if score <= 109:  # noqa: PLR2004
        return "average"
    if score <= 119:  # noqa: PLR2004
        return "high average"
    if score <= 129:  # noqa: PLR2004
        return "high"
    if score <= 139:  # noqa: PLR2004
        return "very high"
    return "extremely high"


def normal_score_to_percentile(score: float, mean: float, std: float) -> float:
    """Converts a score in a normal distribution to a percentile.

    Args:
        score: The score to convert.
        mean: The mean of the normal distribution.
        std: The standard deviation of the normal distribution.

    Returns:
        The percentile of the normal distribution.
    """
    return statistics.NormalDist(mean, std).cdf(float(score)) * 100
