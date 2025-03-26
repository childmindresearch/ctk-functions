"""Module for the WISC tables_old."""

import dataclasses
import functools

from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class WiscCompositeRowLabels:
    """Defines the rows of the composite table.

    Attributes:
        name: Name of the score, used in the first column.
        score_column: Acronym of the row, used in the first
            column and for accessing the SQL data.
    """

    name: str
    score_column: str


WISC_COMPOSITE_ROW_LABELS = (
    WiscCompositeRowLabels(name="Verbal Comprehension (VCI)", score_column="WISC_VCI"),
    WiscCompositeRowLabels(name="Visual Spatial (VSI)", score_column="WISC_VSI"),
    WiscCompositeRowLabels(name="Fluid Reasoning (FRI)", score_column="WISC_FRI"),
    WiscCompositeRowLabels(name="Working Memory (WMI)", score_column="WISC_WMI"),
    WiscCompositeRowLabels(name="Processing Speed (PSI)", score_column="WISC_PSI"),
    WiscCompositeRowLabels(name="Full Scale IQ (FSIQ)", score_column="WISC_FSIQ"),
)


class WiscCompositeDataSource(base.DataProducer):
    """Fetches data for and creates the WISC composite table."""

    @classmethod
    @functools.lru_cache
    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.Wisc5)

        header = [
            base.WordTableCell(content="Composite"),
            base.WordTableCell(content="Standard Score"),
            base.WordTableCell(content="Percentile"),
            base.WordTableCell(content="Range"),
        ]
        content_rows = [
            _create_wisc_composite_row(data, label)
            for label in WISC_COMPOSITE_ROW_LABELS
        ]

        return base.WordTableMarkup(rows=[header, *content_rows])


def _create_wisc_composite_row(
    data: models.Wisc5,
    label: WiscCompositeRowLabels,
) -> list[base.WordTableCell]:
    score = getattr(data, label.score_column)
    percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
    qualifier = utils.standard_score_to_qualifier(score)

    return [
        base.WordTableCell(content=label.name),
        base.WordTableCell(content=score),
        base.WordTableCell(content=f"{percentile:.0f}"),
        base.WordTableCell(content=qualifier),
    ]


class WiscCompositeTable(base.WordTableSection):
    """Renderer for the WISC composite table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the WISC renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = WiscCompositeDataSource.fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content=(
                    "The Wechsler Intelligence Scale for "
                    "Children-Fifth Edition (WISC-V)"
                ),
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the WISC Composite table to the document."""
        self.renderer.add_to(doc)
