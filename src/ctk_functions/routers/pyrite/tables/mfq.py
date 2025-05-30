"""Module for getting the Mood and Feelings Questionnaire table."""

import functools

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import types
from ctk_functions.routers.pyrite.tables import base
from ctk_functions.routers.pyrite.tables.generic import parent_child

MFQ_ROW_LABELS = (
    parent_child.ParentChildRow(
        subscale="Total Score",
        parent_column="MFQ_P_Total",
        child_column="MFQ_SR_Total",
        relevance=[
            base.ClinicalRelevance(
                low=26,
                high=None,
                label=None,
                style=cmi_docx.CellStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
)


class _MfqDataSource(base.DataProducer):
    """Fetches the data for the MFQ table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[types.TestId, ...]:  # noqa: ARG003
        return ("mfq",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the MFQ data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        return parent_child.fetch_parent_child_data(
            mrn,
            models.MfqParent,
            models.MfqSelf,
            MFQ_ROW_LABELS,
        )


class MfqTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Mfq table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Mfq renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _MfqDataSource
        self.formatters = parent_child.fetch_parent_child_formatting(
            row_labels=MFQ_ROW_LABELS
        )
