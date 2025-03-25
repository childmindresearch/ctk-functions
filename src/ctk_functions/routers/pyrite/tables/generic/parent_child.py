from collections.abc import Sequence

import pydantic
import sqlalchemy

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils


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
    eid = utils.mrn_to_eid(mrn)
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

    header = [
        base.WordTableCell(content="Subscales"),
        base.WordTableCell(content="Parent"),
        base.WordTableCell(content="Child"),
        base.WordTableCell(content="Clinical Relevance"),
    ]

    content_rows = [
        _build_parent_child_row(data[0], data[1], label) for label in row_labels
    ]
    return base.WordTableMarkup(rows=[header, *content_rows])


def _build_parent_child_row(
    parent_data: models.Base,
    child_data: models.Base,
    label: ParentChildRow,
) -> list[base.WordTableCell]:
    styles = [
        base.ConditionalStyle(condition=relevance.in_range, style=relevance.style)
        for relevance in label.relevance
    ]
    formatter = base.Formatter(conditional_styles=styles)
    return [
        base.WordTableCell(content=label.subscale),
        base.WordTableCell(
            content=getattr(parent_data, label.parent_column) or "N/A",
            formatter=formatter,
        ),
        base.WordTableCell(
            content=getattr(child_data, label.child_column) or "N/A",
            formatter=formatter,
        ),
        base.WordTableCell(
            content="\n".join(str(relevance) for relevance in label.relevance),
            formatter=base.Formatter(merge_top=True),
        ),
    ]
