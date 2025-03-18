"""Module for inserting the SWAN table."""

import dataclasses
from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used for accessing the SQL data.
        relevance: The limit for clinical relevance.
    """

    name: str
    acronym: str
    relevance: str


# Defines the rows and their order of appearance.
ROW_LABELS = (
    RowLabels(name="ADHD Inattentive", acronym="IN", relevance=">= 1.78"),
    RowLabels(name="ADHD Hyperactive/Impulsive", acronym="HY", relevance=">= 1.44"),
    RowLabels(name="ADHD Total (Combined Type)", acronym="Total", relevance=">= 1.67"),
)


class Swan(base.BaseTable):
    """Fetches and creates the SWAN table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_SWAN_t).where(
            self.eid == models.t_I2B2_Export_SWAN_t.c.EID,  # type: ignore[arg-type]
        )

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the SWAN table to the report.

        Args:
            doc: The word document.
        """
        header_texts = [
            "Subscale",
            "Score",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(ROW_LABELS):
            row = table.rows[index + 1]
            row.cells[0].text = label.name
            row.cells[1].text = "{:.2f}".format(
                getattr(self._data_no_none, f"SWAN_{label.acronym}"),
            )
            row.cells[2].text = label.relevance
