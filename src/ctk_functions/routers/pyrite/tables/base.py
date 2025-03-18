"""Base class definition for all tables."""

import abc
import dataclasses
from collections.abc import Sequence
from typing import Any

import cmi_docx
import fastapi
import sqlalchemy
from docx import document
from starlette import status

from ctk_functions.microservices.sql import client
from ctk_functions.routers.pyrite.tables import utils


class TableDataNotFoundError(Exception):
    """Error raised when table data cannot be found."""


class BaseTable(abc.ABC):
    """Abstract base class for all Pyrite tables."""

    def __init__(self, eid: str) -> None:
        """Initialize the table with an EID.

        Args:
            eid: The unique identifier of the participant.
        """
        self.eid = eid

        self._data: sqlalchemy.Row[tuple[Any, ...]] | None = None
        self._has_fetched_data = False

    @abc.abstractmethod
    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the table to the document.

        Args:
            doc: The Word document.
        """

    @property
    @abc.abstractmethod
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        """The SQL statement for fetching the data."""

    @property
    def data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Fetches the data if it has not been fetched yet."""
        if not self._has_fetched_data:
            self._get_data()
        return self._data

    def _get_data(self) -> None:
        """Cached data property that is only computed on request."""
        with client.get_session() as session:
            rows = session.execute(self._statement).fetchall()

        if len(rows) > 1:
            raise fastapi.HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Found multiple selected rows.",
            )

        self._has_fetched_data = True
        self._data = rows[0]

    @property
    def _data_no_none(self) -> sqlalchemy.Row[tuple[Any, ...]]:
        """Copy of the data that raises an error on None.

        Used to coalesce all None checks in one place.
        """
        if self.data is None:
            msg = "Data is None, cannot add this table."
            raise TableDataNotFoundError(msg)
        return self.data


@dataclasses.dataclass
class TScoreRow:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
    """

    name: str
    column: str
    relevance: Sequence[utils.ClinicalRelevance]


class TScoreTable(BaseTable, abc.ABC):
    """Template for a standard t-score table."""

    def _add_tscore(
        self,
        doc: document.Document,
        labels: Sequence[TScoreRow],
    ) -> None:
        """Adds the t-score table with clinical relevance tothe document..

        Args:
            doc: The Word document.
            labels: The rows of the t-score table.
        """
        header_texts = [
            "Subscale",
            "T-Score",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(labels) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(labels):
            row = table.rows[index + 1]
            row.cells[0].text = label.name
            score = getattr(self._data_no_none, label.column)
            row.cells[1].text = str(score)
            for relevance in label.relevance:
                if relevance.in_range(score):
                    extended_cell = cmi_docx.ExtendCell(table.rows[index + 1].cells[1])
                    extended_cell.format(relevance.style)
                    break

            relevance_text = "\n".join(
                [str(relevance) for relevance in label.relevance],
            )
            utils.set_index_column_name_or_merge(
                table,
                relevance_text,
                row_index=index + 1,
                col_index=2,
            )
