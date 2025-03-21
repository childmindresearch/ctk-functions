"""Module for inserting the Srs table."""

from typing import Any

import cmi_docx
import sqlalchemy

from ctk_functions.routers.pyrite.tables import base, utils

CLINICAL_RELEVANCE = (
    utils.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=60,
        high=75,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=75,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)

# Defines the rows and their order of appearance.
SRS_ROW_LABELS = (
    base.TScoreRow(
        name="Social Awareness",
        column="SRS_AWR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Social Cognition",
        column="SRS_COG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Social Communication",
        column="SRS_COM_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Social Motivation",
        column="SRS_MOT_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Restrictive and Repetitive Behavior",
        column="SRS_RRB_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Total Score",
        column="SRS_Total_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class Srs(base.TScoreTable):
    """Fetches and creates the Srs table."""

    _title = "Social Responsiveness Scale"
    _row_labels = SRS_ROW_LABELS

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_SRS_t).where(
            self.eid == models.t_I2B2_Export_SRS_t.c.EID,  # type: ignore[arg-type]
        )
