"""Module for inserting the CBCL and YSR tables."""

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, tscore

# There are two sets of thresholds for clinical relevance.
# The one with higher scores is denoted as "HIGH", the other as "LOW".
CLINICAL_RELEVANCE_HIGH = [
    base.ClinicalRelevance(
        low=None,
        high=65,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=65,
        high=70,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=70,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]

CLINICAL_RELEVANCE_LOW = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=65,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=65,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


# Defines the rows and their order of appearance.
CBCL_YSR_ROW_LABELS = {
    key: (
        tscore.TScoreRowLabel(
            subscale="Anxious/Depressed",
            score_column=f"{key}_AD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Withdrawn/Depressed",
            score_column=f"{key}_WD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Somatic Complaints",
            score_column=f"{key}_SC_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Social Problems",
            score_column=f"{key}_SP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Thought Problems",
            score_column=f"{key}_TP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Attention Problems",
            score_column=f"{key}_AP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Rule Breaking Behaviors",
            score_column=f"{key}_RBB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Aggressive Behaviors",
            score_column=f"{key}_AB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Internalizing (Emotional) Problems",
            score_column=f"{key}_Int_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        tscore.TScoreRowLabel(
            subscale="Externalizing (Behavioral) Problems",
            score_column=f"{key}_Ext_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        tscore.TScoreRowLabel(
            subscale="Total Problems",
            score_column=f"{key}_Total_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
    )
    for key in ("CBCL", "YSR")
}


class Cbcl(base.PyriteBaseTable):
    """Fetches and creates the Child Behavior Checklist table."""

    def add(self, doc: document.Document) -> None:
        """Add the CBCL table to the provided document.

        Args:
            doc: The Word document to which the table will be added.
        """
        data_source: base.SqlDataSource[models.Cbcl] = base.SqlDataSource(
            query=sqlalchemy.select(models.Cbcl).where(models.Cbcl.EID == self.eid),
        )

        tbl = tscore.build_tscore_table(
            data_source,
            CBCL_YSR_ROW_LABELS["CBCL"],
            title="Child Behavior Checklist - Parent Report Form (CBCL)",
        )
        tbl.add(doc)


class Ysr(base.PyriteBaseTable):
    """Fetches and creates the Youth Self Report table."""

    def add(self, doc: document.Document) -> None:
        """Add the YSR table to the provided document.

        Args:
            doc: The Word document to which the table will be added.
        """
        data_source: base.SqlDataSource[models.Cbcl] = base.SqlDataSource(
            query=sqlalchemy.select(models.Cbcl).where(models.Cbcl.EID == self.eid),
        )
        tbl = tscore.build_tscore_table(
            data_source,
            CBCL_YSR_ROW_LABELS["YSR"],
            title="Child Behavior Checklist - Youth Self Report (YSR)",
        )
        tbl.add(doc)
