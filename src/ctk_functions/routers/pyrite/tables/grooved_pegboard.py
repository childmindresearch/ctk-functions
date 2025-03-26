"""Adds the grooved pegboard table to the document."""

import dataclasses

from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class PegBoardRowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        score_column: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    score_column: str


# Defines the rows and their order of appearance.
PEGBOARD_ROW_LABELS = (
    PegBoardRowLabels(name="Dominant", score_column="peg_z_d"),
    PegBoardRowLabels(name="Non-Dominant", score_column="peg_z_nd"),
)


class GroovedPegboardDataSource(base.DataProducer):
    """Fetches the data for the Grooved Pegboard table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the Grooved Pegboard data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.GroovedPegboard)
        header = [
            base.WordTableCell(content="Grooved Pegboard"),
            base.WordTableCell(content="Z-Score"),
            base.WordTableCell(content="Percentile"),
            base.WordTableCell(content="Range"),
        ]

        content_rows = [
            _create_pegboard_content_row(label, data) for label in PEGBOARD_ROW_LABELS
        ]

        return base.WordTableMarkup(rows=[header, *content_rows])


class GroovedPegboardTable(base.WordTableSection):
    """Renderer for the grooved pegboard table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the grooved pegboard renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = GroovedPegboardDataSource().fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content="Abbreviated Neurocognitive Assessment",
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the grooved pegboard table to the document."""
        self.renderer.add_to(doc)


def _create_pegboard_content_row(
    label: PegBoardRowLabels,
    data: models.GroovedPegboard,
) -> list[base.WordTableCell]:
    """Creates a row for the pegboard table with label, score, percentile, and qualifier.

    Args:
        label: A row label.
        data: The SQL data to extract the score from.

    Returns:
        List of WordTableCell objects forming a table row
    """
    score = float(getattr(data, label.score_column))
    percentile = utils.normal_score_to_percentile(score, mean=0, std=1)
    qualifier = _grooved_pegboard_percentile_to_qualifier(percentile)

    return [
        base.WordTableCell(content=label.name),
        base.WordTableCell(content=f"{score:.2f}"),
        base.WordTableCell(content=f"{percentile:.0f}"),
        base.WordTableCell(content=qualifier),
    ]


def _grooved_pegboard_percentile_to_qualifier(percentile: float) -> str:  # noqa: PLR0911
    """Converts the pegboard z-score to a qualifier."""
    if percentile < 0.01:  # noqa: PLR2004  # noqa: PLR0911
        return "extremely low"
    if percentile <= 3:  # noqa: PLR2004
        return "very low"
    if percentile <= 10:  # noqa: PLR2004
        return "low"
    if percentile <= 24:  # noqa: PLR2004
        return "low average"
    if percentile <= 75:  # noqa: PLR2004
        return "average"
    if percentile <= 90:  # noqa: PLR2004
        return "high average"
    if percentile <= 97:  # noqa: PLR2004
        return "high"
    if percentile <= 98:  # noqa: PLR2004
        return "very high"
    return "extremely high"
