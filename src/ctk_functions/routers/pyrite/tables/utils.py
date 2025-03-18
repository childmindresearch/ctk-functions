"""Utilities for all tables."""

# flake8: noqa: PLR2004
from collections.abc import Iterable
from typing import Self

import cmi_docx
import pydantic
from docx import table

TABLE_STYLE = "Grid Table 7 Colorful"


class ClinicalRelevance(pydantic.BaseModel):
    """Stores the score ranges for clinical relevance.

    Attributes:
        low: Minimum (exclusive) score for this tier of relevance.
        high: Maximum (inclusive) score for this tier of relevance.
        label: Label for this tier of relevance.
        style: Custom cell styling for this tier of relevance.
    """

    low: int | None
    high: int | None
    label: str
    style: cmi_docx.TableStyle

    def in_range(self, value: float) -> bool:
        """Checks if value is within the valid range.

        Excludes low value, includes high value.
        """
        if not self.high:
            return value > self.low  # type: ignore[operator]
        if not self.low:
            return value <= self.high
        return self.low < value <= self.high

    def __str__(self) -> str:
        """String representation of the clinical relevance.

        Returns:
            A string denoting the range for this tier's relevance.

        Example outputs:
            "<65 = LABEL" if low is 65, high is not set.
            ">65 = LABEL" if low is not set and high is 65.
            "65-65 = LABEL" if low is 65 and high is 75.
        """
        if self.low is None:
            value = f"<{self.high}"

        elif self.high is None:
            value = f">{self.low}"
        else:
            value = f"{self.low}-{self.high}"
        return f"{value} = {self.label}"

    @pydantic.model_validator(mode="after")
    def check_low_and_high(self) -> Self:
        """Ascertains low/high are set correctly."""
        if not self.low and not self.high:
            msg = "At least one of low or high must not be None."
            raise ValueError(msg)
        if self.low and self.high and self.low >= self.high:
            msg = "Low must be lower than high."
            raise ValueError(msg)
        return self


def add_header(tbl: table.Table, headers: Iterable[str]) -> None:
    """Adds a standardized header to the table.

    Args:
        tbl: The table to add header to.
        headers: The headers to add to the table.

    """
    for cell, text in zip(tbl.rows[0].cells, headers, strict=True):
        cell.text = text


def set_index_column_name_or_merge(
    tbl: table.Table,
    label: str,
    row_index: int,
    col_index: int = 0,
) -> None:
    """Merges cells if the previous row has the same name.

    Args:
        tbl: The table to modify.
        label: The label to add or merge.
        row_index: The row index of the target cell.
        col_index: The column index of the target cell.
    """
    prev_row = tbl.rows[row_index - 1].cells
    row = tbl.rows[row_index].cells
    if prev_row[col_index].text == label:
        prev_row[col_index].merge(row[col_index])
    else:
        row[col_index].text = label


def standard_score_to_qualifier(score: int) -> str:  # noqa: PLR0911
    """Converts standard score to a qualifier.

    Args:
        score: The standard score to convert.

    Returns:
        The corresponding qualifier.
    """
    if score <= 59:
        return "extremely low"
    if score <= 69:
        return "very low"
    if score <= 79:
        return "low"
    if score <= 89:
        return "low average"
    if score <= 109:
        return "average"
    if score <= 119:
        return "high average"
    if score <= 129:
        return "high"
    if score <= 139:
        return "very high"
    return "extremely high"


def standard_score_to_percentile(score: int) -> int:  # noqa: C901, PLR0911, PLR0912, PLR0915
    """Maps a standard score to a percentile rating.

    Args:
        score: The standard score to be mapped.

    Returns:
        The percentile.
    """
    if score <= 67:
        return 1
    if 68 <= score <= 70:
        return 2
    if 71 <= score <= 72:
        return 3
    if 73 <= score <= 74:
        return 4
    if 75 <= score <= 76:
        return 5
    if score == 77:
        return 6
    if score == 78:
        return 7
    if score == 79:
        return 8
    if score == 80:
        return 9
    if score == 81:
        return 10
    if score == 82:
        return 12
    if score == 83:
        return 13
    if score == 84:
        return 14
    if score == 85:
        return 16
    if score == 86:
        return 18
    if score == 87:
        return 19
    if score == 88:
        return 21
    if score == 89:
        return 23
    if score == 90:
        return 25
    if score == 91:
        return 27
    if score == 92:
        return 30
    if score == 93:
        return 32
    if score == 94:
        return 34
    if score == 95:
        return 37
    if score == 96:
        return 39
    if score == 97:
        return 42
    if score == 98:
        return 45
    if score == 99:
        return 47
    if score == 100:
        return 50
    if score == 101:
        return 53
    if score == 102:
        return 55
    if score == 103:
        return 58
    if score == 104:
        return 61
    if score == 105:
        return 63
    if score == 106:
        return 66
    if score == 107:
        return 68
    if score == 108:
        return 70
    if score == 109:
        return 73
    if score == 110:
        return 75
    if score == 111:
        return 77
    if score == 112:
        return 79
    if score == 113:
        return 81
    if score == 114:
        return 82
    if score == 115:
        return 84
    if score == 116:
        return 86
    if score == 117:
        return 87
    if score == 118:
        return 88
    if score == 119:
        return 90
    if score == 120:
        return 91
    if score == 121:
        return 92
    if score == 122:
        return 93
    if score == 123:
        return 94
    if 124 <= score <= 125:
        return 95
    if 126 <= score <= 127:
        return 96
    if 128 <= score <= 129:
        return 97
    if 130 <= score <= 132:
        return 98
    if score >= 133:
        return 99
    msg = f"Unexpected standard value: {score}"
    raise ValueError(msg)
