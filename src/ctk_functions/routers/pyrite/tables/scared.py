"""Module for inserting the Screen for Child Anxiety Related Disorders table."""

import dataclasses
from typing import Any

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabel:
    """Row definitions for the SCARED table."""

    subscale: str
    parent_column: str
    child_column: str
    relevance: utils.ClinicalRelevance


ROW_LABELS = (
    RowLabel(
        subscale="Panic Disorder/Sig. Somatic Symptoms",
        parent_column="SCARED_P_PN",
        child_column="SCARED_SR_PN",
        relevance=utils.ClinicalRelevance(
            low=6,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    RowLabel(
        subscale="Generalized Anxiety Disorder",
        parent_column="SCARED_P_GD",
        child_column="SCARED_SR_GD",
        relevance=utils.ClinicalRelevance(
            low=8,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    RowLabel(
        subscale="Separation Anxiety Disorder",
        parent_column="SCARED_P_SP",
        child_column="SCARED_SR_SP",
        relevance=utils.ClinicalRelevance(
            low=4,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    RowLabel(
        subscale="Social Anxiety Disorder",
        parent_column="SCARED_P_SC",
        child_column="SCARED_SR_SC",
        relevance=utils.ClinicalRelevance(
            low=7,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    RowLabel(
        subscale="Significant School Avoidance",
        parent_column="SCARED_P_SH",
        child_column="SCARED_SR_SH",
        relevance=utils.ClinicalRelevance(
            low=2,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    RowLabel(
        subscale="Total Score: Anxiety Disorder",
        parent_column="SCARED_P_Total",
        child_column="SCARED_SR_Total",
        relevance=utils.ClinicalRelevance(
            low=24,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
)


class Scared(base.BaseTable):
    """Fetches and creates the Scared table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return (
            sqlalchemy.select(
                models.t_I2B2_Export_SCARED_Parent_t,
                models.t_I2B2_Export_SCARED_Self_t,
            )
            .where(
                self.eid == models.t_I2B2_Export_SCARED_Parent_t.c.EID,  # type: ignore[arg-type]
            )
            .outerjoin(
                models.t_I2B2_Export_SCARED_Self_t,
                models.t_I2B2_Export_SCARED_Parent_t.c.EID
                == models.t_I2B2_Export_SCARED_Self_t.c.EID,
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
        header_texts = [
            "Subscales",
            "Parent",
            "Child",
            "Clinical Relevance",
        ]
        table = doc.add_table(len(ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(ROW_LABELS):
            row = table.rows[index + 1].cells
            row[0].text = label.subscale
            parent_score = getattr(self._data_no_none, label.parent_column)
            child_score = getattr(self._data_no_none, label.child_column)
            row[1].text = str(parent_score)
            row[2].text = str(child_score)
            row[3].text = str(label.relevance)

            if label.relevance.in_range(parent_score):
                cmi_docx.ExtendCell(row[1]).format(label.relevance.style)

            if label.relevance.in_range(child_score):
                cmi_docx.ExtendCell(row[2]).format(label.relevance.style)
