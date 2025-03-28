"""Utility data fetching functions for all tables."""

import dataclasses
import functools
import statistics
from typing import Literal, TypeVar

import fastapi
import sqlalchemy
from starlette import status

from ctk_functions.core.config import get_logger
from ctk_functions.microservices.sql import client, models

TABLE_TITLE_LEVEL = 2
logger = get_logger()


class TableDataNotFoundError(Exception):
    """Thrown when a table's data is not found."""


T = TypeVar("T", bound=models.Base)


@dataclasses.dataclass
class UniqueIdentifiers:
    """Dataclass for the variety of unique identifiers used in HBN."""

    mrn: str
    EID: str
    person_id: str


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

    return UniqueIdentifiers(
        mrn=mrn,
        EID=participant.GUID,
        person_id=participant.person_id,
    )


def fetch_participant_row(
    id_property: Literal["person_id", "EID", "mrn"],
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
    identifier = getattr(mrn_to_ids(mrn), id_property)
    statement = sqlalchemy.select(table).where(
        getattr(table, id_property) == identifier,
    )

    with client.get_session() as session:
        data = session.execute(statement).scalar_one_or_none()

    if data:
        return data

    msg = f"Table data not found for {mrn}."
    raise TableDataNotFoundError(msg)


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
