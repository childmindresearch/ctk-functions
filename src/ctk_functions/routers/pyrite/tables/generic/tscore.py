"""Supports the creation of any t-score table."""

import dataclasses
import functools
from collections.abc import Iterable, Sequence

from docx import shared

import ctk_functions.routers.pyrite.reports.utils
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (shared.Cm(6.5), shared.Cm(2.5), shared.Cm(7.5))


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


def fetch_tscore_formatters(
    row_labels: Sequence[TScoreRowLabel],
    *,
    top_border_rows: Iterable[int] | None = None,
) -> tuple[tuple[base.Formatter, ...], ...]:
    """Fetches the formatters for the t-score tables.

    Args:
        row_labels: Definitions of the table rows, header excluded.
        top_border_rows: Rows with thickened top borders.
    """
    if top_border_rows is None:
        top_border_rows = []

    top_borders = dict.fromkeys(top_border_rows, (base.Styles.THICK_TOP_BORDER,))

    return base.FormatProducer.produce(
        n_rows=len(row_labels) + 1,
        column_widths=COLUMN_WIDTHS,
        cell_styles={
            (row_index + 1, 1): _label_to_conditional_styles(label)
            for row_index, label in enumerate(row_labels)
        },
        row_styles=top_borders,
        merge_top=(2,),
    )


def fetch_tscore_data(
    data: models.Base,
    row_labels: Sequence[TScoreRowLabel],
) -> tuple[tuple[str, ...], ...]:
    """Add the SRS table to the provided document.

    Args:
        data: A row of SQL data to pull the table information from.
        row_labels: Definitions of the table rows, header excluded.

    Returns:
        The t-score table's markup.
    """
    header = ("Subscale", "T-Score", "Clinical Relevance")
    body_rows = _build_tscore_body(data, row_labels)
    return header, *body_rows


def _build_tscore_body(
    data: models.Base,
    row_labels: Sequence[TScoreRowLabel],
) -> tuple[tuple[str, ...], ...]:
    """Builds the body of a t-score table.

    Args:
        data: A row of SQL data to pull the table information from.
        row_labels: Definitions of the table rows, header excluded.

    Returns:
        The cells of the table body as a list of rows.
    """
    content_rows = []
    for label in row_labels:
        score = getattr(data, label.score_column)
        relevance = _label_to_relevance_text(label)
        content_rows.append((label.subscale, f"{score:.0f}", relevance))
    return tuple(content_rows)


def create_data_producer(
    test_ids: tuple[ctk_functions.routers.pyrite.reports.utils.TestId, ...],
    model: type[models.Base],
    labels: Sequence[TScoreRowLabel],
) -> type[base.DataProducer]:
    """Creates a t-score data producer.

    Args:
        test_ids: The test ids for Appendix A.
        model: The SQL model to use.
        labels: Definitions of the table rows, header excluded.

    Returns:
        The data producer.
    """

    class _DataSource(base.DataProducer):
        """Fetches the data for a t-score table."""

        @classmethod
        def test_ids(
            cls, mrn: str
        ) -> tuple[ctk_functions.routers.pyrite.reports.utils.TestId, ...]:  # noqa: ARG003
            return test_ids

        @classmethod
        @functools.lru_cache
        def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
            """Fetches data for the given mrn.

            Args:
                mrn: The participant's unique identifier.

            Returns:
                The text contents of the Word table.
            """
            data = utils.fetch_participant_row("EID", mrn, model)
            return fetch_tscore_data(data, labels)

    return _DataSource
