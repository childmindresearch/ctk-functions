"""Module for inserting the Conners3 table."""

import dataclasses
from typing import Any

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
    """

    name: str
    column: str


# Defines the rows and their order of appearance.
ROW_LABELS = (
    RowLabels(name="Inattention", column="C3SR_IN_T"),
    RowLabels(name="Hyperactivity/Impulsivity", column="C3SR_HY_T"),
    RowLabels(name="Learning Problems", column="C3SR_LP_T"),
    RowLabels(name="Defiance/Aggression", column="C3SR_AG_T"),
    RowLabels(name="Family Relations", column="C3SR_FR_T"),
)


CLINICAL_RELEVANCE = (
    utils.ClinicalRelevance(
        low=None,
        high=57,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=57,
        high=63,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=63,
        high=None,
        label="clinically relevant",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)


class Conners3(base.BaseTable):
    """Fetches and creates the Conners3 table."""

    def _get_data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Fetches the data for the Conners3 table.

        Returns:
            The participant's Conners3 table row.
        """
        statement = sqlalchemy.select(models.t_I2B2_Export_C3SR_t).where(
            self.eid == models.t_I2B2_Export_C3SR_t.c.EID,  # type: ignore[arg-type]
        )
        with client.get_session() as session:
            return session.execute(statement).fetchone()

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the Conners3 table to the report.

        Args:
            doc: The word document.
        """
        header_texts = [
            "Subscale",
            "T-Score",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)
        relevance_text = "\n".join([str(relevance) for relevance in CLINICAL_RELEVANCE])

        for index, label in enumerate(ROW_LABELS):
            row = table.rows[index + 1]
            row.cells[0].text = label.name
            score = getattr(self._data_no_none, label.column)
            row.cells[1].text = str(score)
            for relevance in CLINICAL_RELEVANCE:
                if relevance.in_range(score):
                    extended_cell = cmi_docx.ExtendCell(table.rows[index + 1].cells[1])
                    extended_cell.format(relevance.style)
                    break

            utils.set_index_column_name_or_merge(
                table,
                relevance_text,
                row_index=index + 1,
                col_index=2,
            )
