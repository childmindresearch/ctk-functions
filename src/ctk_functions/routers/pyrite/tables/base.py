"""Base class definition for all tables."""

import abc
import dataclasses
from collections.abc import Sequence
from typing import Any

import cmi_docx
import fastapi
import sqlalchemy
from docx import document
from fastapi import status

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

    def add(self, doc: document.Document) -> None:
        """Adds the table to the document with the title."""
        if self._title:
            doc.add_heading(
                text=self._title,
                level=1,
            )
        self._add(doc)

    @abc.abstractmethod
    def _add(
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
    @abc.abstractmethod
    def _title(self) -> str | None:
        """The title of the table."""

    @property
    def data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Fetches the data if it has not been fetched yet."""
        if self._has_fetched_data:
            return self._data

        with client.get_session() as session:
            rows = session.execute(self._statement).fetchall()

        self._has_fetched_data = True
        if len(rows) > 1:
            raise fastapi.HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Found multiple selected rows.",
            )
        if len(rows) == 1:
            self._data = rows[0]
        return self._data

    @property
    def data_no_none(self) -> sqlalchemy.Row[tuple[Any, ...]]:
        """Copy of the data that raises an error on None.

        Used to coalesce None checks in one place.
        """
        if self.data is None:
            msg = "Data is None, cannot use this table."
            raise TableDataNotFoundError(msg)
        return self.data


@dataclasses.dataclass
class TScoreRow:
    """Defines the rows of the t-score table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
        relevance: A clinical relevance scoring. Used both as the third column
            as well as for styling the second column.
    """

    name: str
    column: str
    relevance: Sequence[utils.ClinicalRelevance]


class TScoreTable(BaseTable, abc.ABC):
    """Template for a standard t-score table."""

    @property
    @abc.abstractmethod
    def _row_labels(self) -> tuple[TScoreRow, ...]:
        """The definitions of the table rows."""

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the t-score table with clinical relevance to the document.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Subscale",
            "T-Score",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(self._row_labels) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(self._row_labels):
            row = table.rows[index + 1]
            row.cells[0].text = label.name
            score = getattr(self.data_no_none, label.column)
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


@dataclasses.dataclass
class ParentChildRow:
    """Row definitions for the SCARED table."""

    subscale: str
    parent_column: str
    child_column: str
    relevance: utils.ClinicalRelevance


class ParentChildTable(BaseTable, abc.ABC):
    """Template for a table scoring parent and child responses."""

    @property
    @abc.abstractmethod
    def _row_labels(self) -> tuple[ParentChildRow, ...]:
        """The definitions of the table rows."""

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds a table with both parent and child columns to the document.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Subscales",
            "Parent",
            "Child",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(self._row_labels) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(self._row_labels):
            row = table.rows[index + 1].cells
            row[0].text = label.subscale
            parent_score = getattr(self.data_no_none, label.parent_column)
            child_score = getattr(self.data_no_none, label.child_column)
            row[1].text = str(parent_score)
            row[2].text = str(child_score)
            row[3].text = str(label.relevance)

            if parent_score and label.relevance.in_range(parent_score):
                cmi_docx.ExtendCell(row[1]).format(label.relevance.style)

            if child_score and label.relevance.in_range(child_score):
                cmi_docx.ExtendCell(row[2]).format(label.relevance.style)
