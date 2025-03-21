"""Module for inserting the CELF5 table."""

from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.routers.pyrite.tables import base, utils


class Celf5(base.BaseTable):
    """Fetches and creates the Clinical Evaluation of Language Fundamentals table."""

    _title = "Language Screening"

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_CELF_t).where(
            self.eid == models.t_I2B2_Export_CELF_t.c.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the CELF 5 table to the report.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Test",
            "Total Score",
            "Age Based Cutoff",
            "Range",
        ]
        table = doc.add_table(2, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        row = table.template_rows[1]
        row.cells[0].text = "CELF-5 Screener"
        row.cells[1].text = str(self.data_no_none.CELF_Total)
        row.cells[2].text = str(self.data_no_none.CELF_CriterionScore)
        row.cells[3].text = (
            "Meets criterion cutoff"
            if self.data_no_none.CELF_ExceedCutoff
            else "Does not meet criterion cutoff"
        )
