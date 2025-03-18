"""Utilities for all tables."""

# flake8: noqa: PLR2004
from collections.abc import Iterable

import cmi_docx
from docx import table
from docx.enum import text as enum_text

TABLE_STYLE = "Grid Table 7 Colorful"


def add_header(tbl: table.Table, headers: Iterable[str]) -> None:
    """Adds a standardized header to the table.

    Args:
        tbl: The table to add header to.
        headers: The headers to add to the table.

    """
    for cell, text in zip(tbl.rows[0].cells, headers, strict=True):
        cell.text = text
        cmi_docx.ExtendCell(cell).format(
            cmi_docx.TableStyle(
                paragraph=cmi_docx.ParagraphStyle(
                    bold=True,
                    alignment=enum_text.WD_ALIGN_PARAGRAPH.CENTER,
                ),
            ),
        )


def set_index_column_name_or_merge(
    table: table.Table,
    label: str,
    row_index: int,
    col_index: int = 0,
) -> None:
    """Merges cells if the previous row has the same name."""
    prev_row = table.rows[row_index - 1].cells
    row = table.rows[row_index].cells
    if prev_row[col_index].text == label:
        prev_row[col_index].merge(row[col_index])
    else:
        row[col_index].text = label


def standard_score_to_qualifier(score: int) -> str:  # noqa: PLR0911
    """Converts standard score to a qualifier."""
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
    """Maps a standard value to a corresponding value based on predefined ranges.

    Args:
        score: The standard value to be mapped.

    Returns:
        The mapped value based on the standard value.
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
