"""Module for inserting the Conners3 table."""

import dataclasses
import functools

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import appendix_a
from ctk_functions.routers.pyrite.tables import base, utils
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


class _Conners3DataSource(base.DataProducer):
    """Fetches the data for the Conners3 table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[appendix_a.TestId, ...]:  # noqa: ARG003
        return ("conners_3",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches Conners3 data for the given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Conners3)
        return tscore.fetch_tscore_data(data, CONNERS3_ROW_LABELS)


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
        self.data_source = _Conners3DataSource
        self.formatters = tscore.fetch_tscore_formatters(row_labels=CONNERS3_ROW_LABELS)
