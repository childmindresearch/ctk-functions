"""Module for inserting the SWAN table."""

import dataclasses
import functools

import cmi_docx

import ctk_functions.routers.pyrite.reports.utils
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils
from ctk_functions.routers.pyrite.tables.scq import COLUMN_WIDTHS


@dataclasses.dataclass
class _SwanRowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        relevance: The limit for clinical relevance.
    """

    name: str
    relevance: base.ClinicalRelevance


# Defines the rows and their order of appearance.
SWAN_ROW_LABELS = (
    _SwanRowLabels(
        name="ADHD Inattentive",
        relevance=base.ClinicalRelevance(
            low=1.78,
            high=None,
            label=None,
            low_inclusive=True,
            style=cmi_docx.CellStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    _SwanRowLabels(
        name="ADHD Hyperactive/Impulsive",
        relevance=base.ClinicalRelevance(
            low=1.44,
            high=None,
            label=None,
            low_inclusive=True,
            style=cmi_docx.CellStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    _SwanRowLabels(
        name="ADHD Total (Combined Type)",
        relevance=base.ClinicalRelevance(
            low=1.67,
            high=None,
            label=None,
            low_inclusive=True,
            style=cmi_docx.CellStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
)


class _SwanDataSource(base.DataProducer):
    """Fetches and creates the SWAN table."""

    @classmethod
    def test_ids(
        cls, mrn: str
    ) -> tuple[ctk_functions.routers.pyrite.reports.utils.TestId, ...]:  # noqa: ARG003
        return ("swan",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the SWAN data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Swan)
        header = ("Subscale", "Score", "Clinical Relevance")

        # Scores are clipped at 0, the total needs to be adjusted for clipped scores.
        scores = (
            max(data.SWAN_IN, 0),
            max(data.SWAN_HY, 0),
            (max(data.SWAN_IN, 0) + max(data.SWAN_HY, 0)) / 2,
        )

        content_rows = [
            (label.name, f"{score:.2f}", str(label.relevance))
            for score, label in zip(scores, SWAN_ROW_LABELS, strict=False)
        ]
        return header, *content_rows


class SwanTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Swan table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Swan renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _SwanDataSource

        relevance_styles = {
            (index + 1, 1): (
                base.ConditionalStyle(
                    condition=label.relevance.in_range,
                    style=label.relevance.style,
                ),
            )
            for index, label in enumerate(SWAN_ROW_LABELS)
        }

        self.formatters = base.FormatProducer.produce(
            n_rows=len(SWAN_ROW_LABELS) + 1,
            column_widths=COLUMN_WIDTHS,
            cell_styles=relevance_styles,
        )
