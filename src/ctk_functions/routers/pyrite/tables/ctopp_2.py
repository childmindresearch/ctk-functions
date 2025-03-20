"""Adds the grooved pegboard table to the document."""

import dataclasses
from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class Ctopp2RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    acronym: str


# Defines the rows and their order of appearance.
CTOPP2_ROW_LABELS = (
    Ctopp2RowLabels(name="Rapid Digit Naming", acronym="RD"),
    Ctopp2RowLabels(name="Rapid Letter Naming", acronym="RL"),
    Ctopp2RowLabels(name="Rapid Object Naming", acronym="RO"),
    Ctopp2RowLabels(name="Rapid Color Naming", acronym="NR"),
)


class Ctopp2(base.BaseTable):
    """Creates the Comprehensive Test of Phonological Processing table."""

    _title = None

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_CTOPP_t).where(
            self.eid == models.t_I2B2_Export_CTOPP_t.c.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the CTOPP2 table to the report.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "CTOPP - 2 Rapid Naming",
            "Number of Errors",
        ]
        table = doc.add_table(len(CTOPP2_ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(CTOPP2_ROW_LABELS):
            index += 1  # Offset for the header row.  # noqa: PLW2901
            row = table.rows[index].cells
            row[0].text = f"{label.name}"
            score = getattr(self.data_no_none, f"CTOPP_{label.acronym}_S")
            if not score:
                # In case subtest was not done.
                score = "N/A"
            row[1].text = f"{score}"
