"""Module for fetching the Social Communication Questionnaire data."""

import functools

import cmi_docx
from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import appendix_a
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(6.99),
    shared.Cm(2),
    shared.Cm(7.5),
)

RELEVANCE = base.ClinicalRelevance(
    low=10,
    high=None,
    label="Evidence of clinical concern of ASD",
    style=cmi_docx.CellStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
)


class _ScqDataSource(base.DataProducer):
    """Fetches and creates the SCQ table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[appendix_a.TestId, ...]:  # noqa: ARG003
        return ()

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the Scq data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Scq)
        return (
            ("Scale", "Score", "Clinical Relevance"),
            (
                "Social Communication Questionnaire",
                f"{data.SCQ_Total:.0f}",
                str(RELEVANCE),
            ),
        )


class ScqTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Scq table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[appendix_a.TestId, ...]:  # noqa: ARG003
        """The IDs of the tests used to produce this data.

        Args:
            mrn: The MRN of the test data.
        """
        return ()

    def __init__(self, mrn: str) -> None:
        """Initializes the Scq renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _ScqDataSource
        self.formatters = base.FormatProducer.produce(
            n_rows=2,
            column_widths=COLUMN_WIDTHS,
            column_styles={
                1: (
                    base.ConditionalStyle(
                        condition=RELEVANCE.in_range,
                        style=RELEVANCE.style,
                    ),
                )
            },
        )
