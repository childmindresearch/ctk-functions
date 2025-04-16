"""Creates a table for surveys that have separate parent/child responses."""

from collections.abc import Iterable, Sequence
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


def fetch_parent_child_data(
    mrn: str,
    parent_table: type[models.Base],
    child_table: type[models.Base],
    row_labels: Sequence[ParentChildRow],
) -> tuple[tuple[str, ...], ...]:
    """Fetches parent/child table data.

    Args:
        mrn: The participant's unique identifier.
        parent_table: The parent's SQL table.
        child_table: The child's SQL table.
        row_labels: The row labels for the parent/child table.

    Returns:
        The text contents of the Word table.
    """
    data = _parent_child_sql_request(mrn, parent_table, child_table)
    header = ("Subscales", "Parent", "Child", "Clinical Relevance")
    content_rows = [
        _build_parent_child_row(data[0], data[1], label) for label in row_labels
    ]
    return header, *content_rows


def fetch_parent_child_formatting(
    row_labels: Sequence[ParentChildRow],
    *,
    top_border_rows: Iterable[int] | None = None,
) -> tuple[tuple[base.Formatter, ...], ...]:
    """Fetches parent/child table formatting.

    Args:
        row_labels: The row labels for the parent/child table.
        top_border_rows: Rows with thickened top borders.

    Returns:
        The formatting for the parent/child data.
    """
    relevance_styles = {
        (row_index + 1, col_index): (
            base.ConditionalStyle(
                condition=relevance.in_range,
                style=relevance.style,
            ),
        )
        for col_index in (1, 2)
        for row_index, label in enumerate(row_labels)
        for relevance in label.relevance
    }
    if top_border_rows is None:
        top_border_rows = []
    row_styles = dict.fromkeys(top_border_rows, (base.Styles.THICK_TOP_BORDER.value,))
    return base.FormatProducer.produce(
        n_rows=len(row_labels) + 1,
        column_widths=COLUMN_WIDTHS,
        row_styles=row_styles,
        cell_styles=relevance_styles,
    )


def _parent_child_sql_request(
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
        raise base.TableDataNotFoundError(msg)
    return data


def _build_parent_child_row(
    parent_data: models.Base | None,
    child_data: models.Base | None,
    label: ParentChildRow,
) -> tuple[str, str, str, str]:
    def score2label(data: models.Base | None, column: str) -> str:
        if not data:
            return "N/A"
        score = getattr(data, column)
        if score is None:
            return "N/A"
        return str(score)

    parent_label = score2label(parent_data, label.parent_column)
    child_label = score2label(child_data, label.child_column)
    relevance = "\n".join(str(relevance) for relevance in label.relevance)

    return label.subscale, parent_label, child_label, relevance
