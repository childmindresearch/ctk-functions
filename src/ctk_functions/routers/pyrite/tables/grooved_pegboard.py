"""Adds the grooved pegboard table to the document."""

import bisect
import dataclasses
from typing import Any

import fastapi
import sqlalchemy
from docx import document
from starlette import status

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    acronym: str


# Defines the rows and their order of appearance.
ROW_LABELS = (
    RowLabels(name="Dominant", acronym="d"),
    RowLabels(name="Non-Dominant", acronym="nd"),
)


class GroovedPegboard(base.BaseTable):
    """Fetches and creates the Grooved Pegboard table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(
            models.t_I2B2_Export_GroovedPeg_t,
        ).where(
            self.eid == models.t_I2B2_Export_GroovedPeg_t.c.EID,  # type: ignore[arg-type]
        )

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the grooved pegboard tables to the report.

        Args:
            doc: The word document.
        """
        header_texts = [
            "Grooved Pegboard",
            "Z-Score",
            "Percentile",
            "Range",
        ]
        table = doc.add_table(len(ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(ROW_LABELS):
            index += 1  # Offset for the header row.  # noqa: PLW2901
            row = table.rows[index].cells
            row[0].text = f"{label.name}"
            score = getattr(self._data_no_none, f"peg_z_{label.acronym}")
            percentile = _grooved_pegboard_score_to_percentile(score)
            row[1].text = f"{score:.2f}"
            row[2].text = str(percentile)
            row[3].text = str(_grooved_pegboard_percentile_to_qualifier(percentile))


def _grooved_pegboard_score_to_percentile(score: float) -> int:
    if score > 2.4:  # noqa: PLR2004
        return 99

    z_percentile_map = [
        (-2.1, 1),
        (-1.8, 2),
        (-1.7, 3),
        (-1.6, 4),
        (-1.5, 5),
        (-1.4, 6),
        (-1.3, 8),
        (-1.2, 9),
        (-1.1, 11),
        (-1.0, 13),
        (-0.9, 15),
        (-0.8, 17),
        (-0.7, 20),
        (-0.6, 23),
        (-0.5, 26),
        (-0.4, 29),
        (-0.3, 33),
        (-0.2, 36),
        (-0.1, 42),
        (0.0, 48),
        (0.1, 52),
        (0.2, 56),
        (0.3, 60),
        (0.4, 64),
        (0.5, 67),
        (0.6, 71),
        (0.7, 74),
        (0.8, 77),
        (0.9, 80),
        (1.0, 83),
        (1.1, 86),
        (1.2, 88),
        (1.3, 90),
        (1.4, 91),
        (1.5, 93),
        (1.6, 94),
        (1.7, 95),
        (1.8, 96),
        (1.9, 97),
        (2.0, 97),
        (2.1, 97),
        (2.4, 98),
    ]

    breakpoints = [b for b, p in z_percentile_map]
    idx = bisect.bisect_left(breakpoints, score)

    return z_percentile_map[idx][1]


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
    if percentile == 98:  # noqa: PLR2004
        return "very high"
    if percentile == 99:  # noqa: PLR2004
        return "extremely high"
    raise fastapi.HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unknown pegboard percentile.",
    )
