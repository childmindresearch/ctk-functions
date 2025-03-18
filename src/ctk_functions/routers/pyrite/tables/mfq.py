"""Module for inserting the Mood and Feelings Questionnaire table."""

from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


class Mfq(base.BaseTable):
    """Fetches and creates the MFQ table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return (
            sqlalchemy.select(
                models.t_I2B2_Export_MFQ_Parent_t,
                models.t_I2B2_Export_MFQ_Self_t,
            )
            .where(
                self.eid == models.t_I2B2_Export_MFQ_Parent_t.c.EID,  # type: ignore[arg-type]
            )
            .outerjoin(
                models.t_I2B2_Export_MFQ_Self_t,
                models.t_I2B2_Export_MFQ_Parent_t.c.EID
                == models.t_I2B2_Export_MFQ_Self_t.c.EID,
            )
        )

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds MFQtable to document.

        Args:
            doc: The Word document.
        """
        doc.add_paragraph("Age Norms:")
        header_texts = [
            "Subscales",
            "Parent",
            "Child",
            "Clinical Relevance",
        ]
        table = doc.add_table(2, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        row = table.rows[1].cells
        row[0].text = "Total Score"
        row[1].text = str(self._data_no_none.MFQ_P_Total)
        row[2].text = str(self._data_no_none.MFQ_SR_Total)
        row[3].text = ">26 = cutoff for clinical concern"
