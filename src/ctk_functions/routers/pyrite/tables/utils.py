"""Utility data fetching functions for all tables."""

import statistics
from typing import TypeVar

import cmi_docx

from ctk_functions.core.config import get_logger
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base

logger = get_logger()

T = TypeVar("T", bound=models.Base)


def add_thick_top_border(
    markup: base.WordTableMarkup, row_index: int
) -> base.WordTableMarkup:
    """Convenience function for adding a thicker top borderline within a table.

    Args:
        markup: The Word table markup.
        row_index: The row index above which a thicker border will be added.

    Returns:
        New markup with a thicker top borderline added.
    """
    thick_top_border = base.ConditionalCellStyle(
        style=cmi_docx.CellStyle(
            borders=[
                cmi_docx.CellBorder(
                    sides=("top",),
                    sz=16,  # 2pt
                )
            ]
        )
    )
    for cell in markup.rows[row_index]:
        cell.formatter.conditional_cell_styles.append(thick_top_border)
    return markup


def standard_score_to_qualifier(score: float) -> str:  # noqa: PLR0911
    """Converts standard score to a qualifier.

    This was built with a mean of 100, and std of 15 as the underlying
    normal distribution.

    Args:
        score: The standard score to convert.

    Returns:
        The corresponding qualifier.
    """
    if score <= 59:  # noqa: PLR2004
        return "extremely low"
    if score <= 69:  # noqa: PLR2004
        return "very low"
    if score <= 79:  # noqa: PLR2004
        return "low"
    if score <= 89:  # noqa: PLR2004
        return "low average"
    if score <= 109:  # noqa: PLR2004
        return "average"
    if score <= 119:  # noqa: PLR2004
        return "high average"
    if score <= 129:  # noqa: PLR2004
        return "high"
    if score <= 139:  # noqa: PLR2004
        return "very high"
    return "extremely high"


def normal_score_to_percentile(score: float, mean: float, std: float) -> float:
    """Converts a score in a normal distribution to a percentile.

    Args:
        score: The score to convert.
        mean: The mean of the normal distribution.
        std: The standard deviation of the normal distribution.

    Returns:
        The percentile of the normal distribution.
    """
    return statistics.NormalDist(mean, std).cdf(float(score)) * 100
