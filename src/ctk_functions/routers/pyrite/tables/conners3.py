"""Module for inserting the Conners3 table."""

import dataclasses

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base
from ctk_functions.routers.pyrite.tables.generic import tscore


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
    """

    name: str
    column: str


CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=57,
        label="typical range",
        style=cmi_docx.CellStyle(),
    ),
    base.ClinicalRelevance(
        low=57,
        high=63,
        label="borderline range",
        style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=63,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.CellStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]

# Defines the rows and their order of appearance.
CONNERS3_ROW_LABELS = (
    tscore.TScoreRowLabel(
        subscale="Inattention",
        score_column="C3SR_IN_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Hyperactivity/Impulsivity",
        score_column="C3SR_HY_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Learning Problems",
        score_column="C3SR_LP_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Defiance/Aggression",
        score_column="C3SR_AG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Family Relations",
        score_column="C3SR_FR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class Conners3Table(
    base.WordTableSectionAddToMixin,
    base.WordTableSection,
):
    """Renderer for the Conners3 table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Conners3 renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = tscore.create_data_producer(
            test_ids=("conners_3",),
            model=models.Conners3,
            labels=CONNERS3_ROW_LABELS,
        )
        self.formatters = tscore.fetch_tscore_formatters(row_labels=CONNERS3_ROW_LABELS)
