"""Adds the grooved pegboard table to the document."""

import dataclasses
import decimal
import statistics
from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class PegBoardRowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    acronym: str


# Defines the rows and their order of appearance.
PEGBOARD_ROW_LABELS = (
    PegBoardRowLabels(name="Dominant", acronym="d"),
    PegBoardRowLabels(name="Non-Dominant", acronym="nd"),
)


class GroovedPegboard(base.BaseTable):
    """Fetches and creates the Grooved Pegboard table."""

    _title = "Abbreviated Neurocognitive Assessment"

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(
            models.t_I2B2_Export_GroovedPeg_t,
        ).where(
            self.eid == models.t_I2B2_Export_GroovedPeg_t.c.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the grooved pegboard tables to the report.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Grooved Pegboard",
            "Z-Score",
            "Percentile",
            "Range",
        ]
        table = doc.add_table(len(PEGBOARD_ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(PEGBOARD_ROW_LABELS):
            index += 1  # Offset for the header row.  # noqa: PLW2901
            row = table.rows[index].cells
            row[0].text = f"{label.name}"
            score = getattr(self.data_no_none, f"peg_z_{label.acronym}")
            percentile = _zscore_to_percentile(score)
            row[1].text = f"{score:.2f}"
            row[2].text = str(int(percentile))
            row[3].text = (_grooved_pegboard_percentile_to_qualifier(percentile),)


def _zscore_to_percentile(zscore: decimal.Decimal) -> int:
    return int(round((statistics.NormalDist().cdf(float(zscore))) * 100))


def _grooved_pegboard_percentile_to_qualifier(percentile: int) -> str:  # noqa: PLR0911
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
