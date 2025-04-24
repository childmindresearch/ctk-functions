"""Definition of the Social Responsiveness Scale table."""

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base
from ctk_functions.routers.pyrite.tables.generic import tscore

CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.CellStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=75,
        label="borderline range",
        style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=75,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.CellStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


# Defines the rows and their order of appearance.
SRS_ROW_LABELS = (
    tscore.TScoreRowLabel(
        subscale="Social Awareness",
        score_column="SRS_AWR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Cognition",
        score_column="SRS_COG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Communication",
        score_column="SRS_COM_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Motivation",
        score_column="SRS_MOT_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Restrictive and Repetitive Behavior",
        score_column="SRS_RRB_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Total Score",
        score_column="SRS_Total_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class SrsTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Srs table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Srs renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = tscore.create_data_producer(
            test_ids=("srs",), model=models.Srs, labels=SRS_ROW_LABELS
        )
        self.formatters = tscore.fetch_tscore_formatters(
            row_labels=SRS_ROW_LABELS, top_border_rows=(-1,)
        )
