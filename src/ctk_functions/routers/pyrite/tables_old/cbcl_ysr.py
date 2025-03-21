"""Module for inserting the CBCL and YSR tables."""

from typing import Any

import cmi_docx
import sqlalchemy

from ctk_functions.routers.pyrite.tables import base, utils

# There are two sets of thresholds for clinical relevance.
# The one with higher scores is denoted as "HIGH", the other as "LOW".
CLINICAL_RELEVANCE_HIGH = (
    utils.ClinicalRelevance(
        low=None,
        high=65,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=65,
        high=70,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=70,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)

CLINICAL_RELEVANCE_LOW = (
    utils.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=60,
        high=65,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=65,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)


# Defines the rows and their order of appearance.
CBCL_YSR_ROW_LABELS = {
    key: (
        base.TScoreRow(
            name="Anxious/Depressed",
            column=f"{key}_AD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Withdrawn/Depressed",
            column=f"{key}_WD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Somatic Complaints",
            column=f"{key}_SC_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Social Problems",
            column=f"{key}_SP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Thought Problems",
            column=f"{key}_TP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Attention Problems",
            column=f"{key}_AP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Rule Breaking Behaviors",
            column=f"{key}_RBB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Aggressive Behaviors",
            column=f"{key}_AB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        base.TScoreRow(
            name="Internalizing (Emotional) Problems",
            column=f"{key}_Int_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        base.TScoreRow(
            name="Externalizing (Behavioral) Problems",
            column=f"{key}_Ext_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        base.TScoreRow(
            name="Total Problems",
            column=f"{key}_Total_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
    )
    for key in ("CBCL", "YSR")
}


class Cbcl(base.TScoreTable):
    """Fetches and creates the Child Behavior Checklist table."""

    _title = "Child Behavior Checklist - Parent Report Form (CBCL)"
    _row_labels = CBCL_YSR_ROW_LABELS["CBCL"]

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(
            models.t_I2B2_Export_CBCL_t,
        ).where(
            self.eid == models.t_I2B2_Export_CBCL_t.c.EID,  # type: ignore[arg-type]
        )


class Ysr(base.TScoreTable):
    """Fetches and creates the Youth Self Report table."""

    _title = "Child Behavior Checklist - Youth Self Report (YSR)"
    _row_labels = CBCL_YSR_ROW_LABELS["YSR"]

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(
            models.t_I2B2_Export_YSR_t,
        ).where(
            self.eid == models.t_I2B2_Export_YSR_t.c.EID,  # type: ignore[arg-type]
        )
