"""Supports the creation of any t-score table."""

import dataclasses
import functools
from collections.abc import Callable, Sequence
from typing import TypeVar

from ctk_functions.routers.pyrite.tables import base

T = TypeVar("T")


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
    data_source: base.SqlDataSource[T],
    rows: Sequence[TScoreRowLabel],
    title: str | None = None,
) -> base.WordDocumentTableRenderer[T]:
    """Add the SRS table to the provided document.

    Args:
        data_source: The Sql data source from which to pull the data.
        rows: The rows to include in the table.
        title: The title of the table.

    """
    header: list[base.TableCell[str]] = [
        base.TableCell(content="Subscale"),
        base.TableCell(content="T-Score"),
        base.TableCell(content="Clinical Relevance"),
    ]
    content_rows: list[list[base.TableCell[str | Callable[[T], str]]]] = [
        [
            base.TableCell(content=label.subscale),
            base.TableCell(
                content=functools.partial(
                    lambda row, lbl: getattr(row, lbl.score_column),
                    lbl=label,
                ),
                formatter=base.Formatter(
                    conditional_styles=_label_to_conditional_styles(label),
                ),
            ),
            base.TableCell(
                content=_label_to_relevance_text(label),
                formatter=base.Formatter(merge_top=True),
            ),
        ]
        for label in rows
    ]
    template_rows = [header, *content_rows]

    return base.WordDocumentTableRenderer(
        data_source=data_source,
        template_rows=template_rows,
        title=title,
    )
