"""Module for inserting the Gilliam Autism Rating Scale table."""

from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


class Gars(base.BaseTable):
    """Fetches and creates the GARS table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_GARS_t).where(
            self.eid == models.t_I2B2_Export_GARS_t.c.EID,  # type: ignore[arg-type]
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
            "Autism Index Score",
            "Percentile Rank",
            "Autism Index Interpretation",
        ]
        table = doc.add_table(2, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        row = table.rows[1]
        row.cells[0].text = str(self._data_no_none.GARS_AI)
        row.cells[1].text = str(self._data_no_none.GARS_AI_Perc)
        row.cells[2].text = (
            "<60 = typical range\n60-75 = borderline range\n>75 = "
            "clinically relevant impairment"
        )
        doc.add_paragraph(
            "*Caution is advised in interpretation of the Autism Index score, because "
            "individuals with other diagnoses including ADHD, ODD, anxiety, language "
            "disorder, and intellectual disability, may demonstrate behaviors typical "
            "of individuals diagnosed with autism. Thus, clinically elevated scores on "
            "this assessment are not necessarily indicative of an autism diagnosis",
        )
