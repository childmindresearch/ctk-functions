"""Module for inserting the Social Communication Questionnaire table."""

from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.routers.pyrite.tables import base, utils


class Scq(base.BaseTable):
    """Fetches and creates the SCQ table."""

    _title = "Social Communication Questionnaire"

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_SCQ_t).where(
            self.eid == models.t_I2B2_Export_SCQ_t.c.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the SCQ table to the report.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Scale",
            "Score",
            "Clinical Relevance",
        ]
        table = doc.add_table(2, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        row = table.template_rows[1]
        row.cells[0].text = "Social Communication Questionnaire"
        score = self.data_no_none.SCQ_Total
        row.cells[1].text = str(score)
        row.cells[2].text = ">10: Evidence for clinical concern of ASD"
