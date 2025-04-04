"""Supports the creation of any t-score table."""

import dataclasses
from collections.abc import Sequence

from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base

COLUMN_WIDTHS = (shared.Cm(6.5), shared.Cm(3.5), shared.Cm(6.5))


@dataclasses.dataclass
class TScoreRowLabel:
    """Defines a row for the SRS Table.

    Attributes:
        subscale: The name to display for this subscale.
        score_column: The name of the column that contains the t-score.
        relevance: The clinical relevance thresholds to check.
    """

    subscale: str
    score_column: str
    relevance: list[base.ClinicalRelevance] = dataclasses.field(default_factory=list)


def _label_to_relevance_text(label: TScoreRowLabel) -> str:
    """Gets the relevance text for a row.

    Args:
        label: The row definition.

    Returns:
        The relevance text.
    """
    return "\n".join(str(rele) for rele in label.relevance)


def _label_to_conditional_styles(label: TScoreRowLabel) -> list[base.ConditionalStyle]:
    """Gets the conditional styles for a row.

    Args:
        label: The row definition.

    Returns:
        The conditional styles.
    """
    return [
        base.ConditionalStyle(
            condition=rele.in_range,
            style=rele.style,
        )
        for rele in label.relevance
    ]


def build_tscore_table(
    data: models.Base,
    row_labels: Sequence[TScoreRowLabel],
) -> base.WordTableMarkup:
    """Add the SRS table to the provided document.

    Args:
        data: A row of SQL data to pull the table information from.
        row_labels: Definitions of the table rows, header excluded.

    """
    header_formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
    header_content = ["Subscale", "T-Score", "Clinical Relevance"]
    header = [
        base.WordTableCell(content=content, formatter=formatter)
        for content, formatter in zip(header_content, header_formatters, strict=True)
    ]

    content_rows = [
        [
            base.WordTableCell(
                content=label.subscale, formatter=base.Formatter(width=COLUMN_WIDTHS[0])
            ),
            base.WordTableCell(
                content=getattr(data, label.score_column),
                formatter=base.Formatter(
                    conditional_styles=_label_to_conditional_styles(label),
                    width=COLUMN_WIDTHS[1],
                ),
            ),
            base.WordTableCell(
                content=_label_to_relevance_text(label),
                formatter=base.Formatter(merge_top=True, width=COLUMN_WIDTHS[2]),
            ),
        ]
        for label in row_labels
    ]
    template_rows = [header, *content_rows]

    return base.WordTableMarkup(rows=template_rows)
