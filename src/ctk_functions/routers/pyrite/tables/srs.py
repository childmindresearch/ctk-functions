"""Definition of the Social Responsiveness Scale table."""

import functools

import cmi_docx
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils
from ctk_functions.routers.pyrite.tables.generic import tscore

CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=75,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=75,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
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


class SrsDataSource(base.DataProducer):
    """Fetches the data for the SRS table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches SRS data for the given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Srs)
        return tscore.build_tscore_table(data, SRS_ROW_LABELS)


class SrsTable(base.WordTableSection, data_source=SrsDataSource):
    """Renderer for the Srs table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Srs renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.preamble = [
            base.ParagraphBlock(
                content="Social Responsiveness Scale",
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]

    def add_to(self, doc: document.Document) -> None:
        """Adds the Srs table to the document."""
        markup = self.data_source.fetch(self.mrn)
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        renderer = base.WordDocumentTableSectionRenderer(
            preamble=self.preamble,
            table_renderer=table_renderer,
        )
        renderer.add_to(doc)
