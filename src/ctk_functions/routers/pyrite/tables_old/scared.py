"""Module for inserting the Screen for Child Anxiety Related Disorders table."""

from typing import Any

import cmi_docx
import sqlalchemy

from ctk_functions.routers.pyrite.tables import base, utils

SCARED_ROW_LABELS = (
    base.ParentChildRow(
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
    base.ParentChildRow(
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
    base.ParentChildRow(
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
    base.ParentChildRow(
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
    base.ParentChildRow(
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
    base.ParentChildRow(
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


class Scared(base.ParentChildTable):
    """Fetches and creates the Scared table."""

    _title = "Screen for Child Anxiety Related Disorders"
    _row_labels = SCARED_ROW_LABELS

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
