"""Module for inserting the SWAN table."""

import dataclasses
import functools

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


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
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    _SwanRowLabels(
        name="ADHD Hyperactive/Impulsive",
        relevance=base.ClinicalRelevance(
            low=1.44,
            high=None,
            label=None,
            low_inclusive=True,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
    _SwanRowLabels(
        name="ADHD Total (Combined Type)",
        relevance=base.ClinicalRelevance(
            low=1.67,
            high=None,
            label=None,
            low_inclusive=True,
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        ),
    ),
)


class _SwanDataSource(base.DataProducer):
    """Fetches and creates the SWAN table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the SWAN data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Swan)
        header = [
            base.WordTableCell(content="Subscale"),
            base.WordTableCell(content="Score"),
            base.WordTableCell(content="Clinical Relevance"),
        ]

        # Scores are clipped at 0, the total needs to be adjusted for clipped scores.
        scores = (
            max(data.SWAN_IN, 0),
            max(data.SWAN_HY, 0),
            (max(data.SWAN_IN, 0) + max(data.SWAN_HY, 0)) / 2,
        )

        content_rows = [
            [
                base.WordTableCell(content=label.name),
                base.WordTableCell(
                    content=f"{score:.2f}",
                    formatter=base.Formatter(
                        conditional_styles=[
                            base.ConditionalStyle(
                                condition=label.relevance.in_range,
                                style=label.relevance.style,
                            ),
                        ],
                    ),
                ),
                base.WordTableCell(content=str(label.relevance)),
            ]
            for score, label in zip(scores, SWAN_ROW_LABELS, strict=False)
        ]
        return base.WordTableMarkup(rows=[header, *content_rows])


class SwanTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Swan table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Swan renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.preamble = [
            base.ParagraphBlock(
                content=(
                    "Strengths and Weaknesses of ADHD Symptoms "
                    "and Normal Behavior (SWAN)"
                ),
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        self.data_source = _SwanDataSource
