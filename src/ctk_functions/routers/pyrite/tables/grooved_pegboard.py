"""Adds the grooved pegboard table to the document."""

import dataclasses
import functools

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class _PegBoardRowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        score_column: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    score_column: str


# Defines the rows and their order of appearance.
PEGBOARD_ROW_LABELS = (
    _PegBoardRowLabels(name="Dominant", score_column="peg_z_d"),
    _PegBoardRowLabels(name="Non-Dominant", score_column="peg_z_nd"),
)


class _GroovedPegboardDataSource(base.DataProducer):
    """Fetches the data for the Grooved Pegboard table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the Grooved Pegboard data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.GroovedPegboard)
        header = ("Hand", "Z-Score", "Percentile", "Range")
        content_rows = [
            _create_pegboard_content_row(label, data) for label in PEGBOARD_ROW_LABELS
        ]
        return header, *content_rows


class GroovedPegboardTable(
    base.WordTableSectionAddToMixin,
    base.WordTableSection,
):
    """Renderer for the grooved pegboard table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the grooved pegboard renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _GroovedPegboardDataSource
        self.formatters = base.FormatProducer.produce(
            n_rows=len(PEGBOARD_ROW_LABELS) + 1, column_widths=[None] * 4
        )


def _create_pegboard_content_row(
    label: _PegBoardRowLabels,
    data: models.GroovedPegboard,
) -> tuple[str, str, str, str]:
    """Creates a row for the pegboard table.

    Args:
        label: A row label.
        data: The SQL data to extract the score from.

    Returns:
        List of WordTableCell objects forming a table row
    """
    score = float(getattr(data, label.score_column))
    percentile = utils.normal_score_to_percentile(score, mean=0, std=1)
    qualifier = _grooved_pegboard_percentile_to_qualifier(percentile)

    return label.name, f"{score:.2f}", f"{percentile:.0f}", qualifier


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
