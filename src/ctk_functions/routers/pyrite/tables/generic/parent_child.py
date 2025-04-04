"""Creates a table for surveys that have separate parent/child responses."""

from collections.abc import Sequence
from typing import TypeVar

import pydantic
import sqlalchemy
from docx import shared

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(6.99),
    shared.Cm(2.76),
    shared.Cm(2.73),
    shared.Cm(4.02),
)

T_parent = TypeVar("T_parent", bound=models.Base)
T_child = TypeVar("T_child", bound=models.Base)


class ParentChildRow(pydantic.BaseModel):
    """Row definitions for tables containing child and parent responses."""

    subscale: str
    parent_column: str
    child_column: str
    relevance: list[base.ClinicalRelevance]


def build_parent_child_table(
    mrn: str,
    parent_table: type[models.Base],
    child_table: type[models.Base],
    row_labels: Sequence[ParentChildRow],
) -> base.WordTableMarkup:
    """Creates a parent/child table.

    Args:
        mrn: The participant's unique identifier.
        parent_table: The parent's SQL table.
        child_table: The child's SQL table.
        row_labels: The row labels for the parent/child table.

    Returns:
        The markup for the parent/child table.
    """
    data = _get_parent_child_data(mrn, parent_table, child_table)

    formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
    content = ["Subscales", "Parent", "Child", "Clinical Relevance"]
    header = [
        base.WordTableCell(content=content, formatter=formatter)
        for content, formatter in zip(content, formatters, strict=True)
    ]

    content_rows = [
        _build_parent_child_row(data[0], data[1], label) for label in row_labels
    ]
    return base.WordTableMarkup(rows=[header, *content_rows])


def _get_parent_child_data(
    mrn: str, parent_table: type[T_parent], child_table: type[T_child]
) -> sqlalchemy.Row[tuple[T_parent, T_child]]:
    eid = utils.mrn_to_ids(mrn).EID
    statement = (
        sqlalchemy.select(
            parent_table,
            child_table,
        )
        .where(
            parent_table.EID == eid,  # type: ignore[attr-defined]
        )
        .outerjoin(
            child_table,
            parent_table.EID == child_table.EID,  # type: ignore[attr-defined]
        )
    )
    with client.get_session() as session:
        data = session.execute(statement).fetchone()
    if not data:
        msg = f"Could not find MFQ data for {mrn}."
        raise utils.TableDataNotFoundError(msg)
    return data


def _build_parent_child_row(
    parent_data: models.Base | None,
    child_data: models.Base | None,
    label: ParentChildRow,
) -> list[base.WordTableCell]:
    styles = [
        base.ConditionalStyle(condition=relevance.in_range, style=relevance.style)
        for relevance in label.relevance
    ]
    formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
    formatters[1].conditional_styles.extend(styles)
    formatters[2].conditional_styles.extend(styles)

    def score2label(data: models.Base | None, column: str) -> str:
        if not data:
            return "N/A"
        score = getattr(data, column)
        if score is None:
            return "N/A"
        return str(score)

    parent_label = score2label(parent_data, label.parent_column)
    child_label = score2label(child_data, label.child_column)

    return [
        base.WordTableCell(content=label.subscale, formatter=formatters[0]),
        base.WordTableCell(content=parent_label, formatter=formatters[1]),
        base.WordTableCell(content=child_label, formatter=formatters[2]),
        base.WordTableCell(
            content="\n".join(str(relevance) for relevance in label.relevance),
            formatter=formatters[3],
        ),
    ]
