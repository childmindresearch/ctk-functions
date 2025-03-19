"""Module for inserting the Mood and Feelings Questionnaire table."""

from typing import Any

import cmi_docx
import sqlalchemy

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils

ROW_LABELS = (
    base.ParentChildRow(
        subscale="Total Score",
        parent_column="MFQ_P_Total",
        child_column="MFQ_SR_Total",
        relevance=utils.ClinicalRelevance(
            low=26,
            high=None,
            label=None,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
)


class Mfq(base.ParentChildTable):
    """Fetches and creates the MFQ table."""

    _title = "Mood and Feelings Questionnaire (MFQ) - Long Version"
    _row_labels = ROW_LABELS

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
