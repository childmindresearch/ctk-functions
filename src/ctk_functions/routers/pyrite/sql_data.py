"""Utility functions for fetching data from the SQL database."""

import dataclasses
import functools
from typing import Literal, TypeVar

import fastapi
import sqlalchemy
from starlette import status

from ctk_functions.core import config
from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base

logger = config.get_logger()

T = TypeVar("T")


@dataclasses.dataclass
class UniqueIdentifiers:
    """Dataclass for the variety of unique identifiers used in HBN."""

    MRN: str
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
    sanitized_mrn = mrn.replace("\r", "").replace("\n", "")
    logger.debug("Fetching participant %s.", sanitized_mrn)
    with client.get_session() as session:
        participant = session.execute(
            sqlalchemy.select(models.CmiHbnIdTrack).where(
                models.CmiHbnIdTrack.MRN == mrn,
            ),
        ).scalar_one_or_none()

    if not participant:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MRN {sanitized_mrn} could not be converted to EID.",
        )

    logger.debug("Fetched participant %s.", sanitized_mrn)
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
    sanitized_mrn = mrn.replace("\r", "").replace("\n", "")
    logger.debug("Fetching table %s, participant %s.", table.__name__, sanitized_mrn)
    identifier = getattr(mrn_to_ids(mrn), id_property)
    statement = sqlalchemy.select(table).where(
        getattr(table, id_property) == identifier,
    )

    with client.get_session() as session:
        data = session.execute(statement).scalar_one_or_none()

    logger.debug("Fetched table %s, participant %s.", table.__name__, sanitized_mrn)
    if data:
        return data

    msg = f"Table data not found for {sanitized_mrn}."
    raise base.TableDataNotFoundError(msg)
