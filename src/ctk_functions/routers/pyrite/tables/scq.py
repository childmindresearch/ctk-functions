"""Module for fetching the Social Communication Questionnaire data."""

import functools

import cmi_docx
from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(6.99),
    shared.Cm(2),
    shared.Cm(7.5),
)


class _ScqDataSource(base.DataProducer):
    """Fetches and creates the SCQ table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the Scq data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Scq)
        relevance = base.ClinicalRelevance(
            low=10,
            high=None,
            label="Evidence of clinical concern of ASD",
            style=cmi_docx.CellStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        )

        formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        formatters[1].conditional_styles.append(
            base.ConditionalStyle(
                condition=relevance.in_range,
                style=relevance.style,
            )
        )

        header = [
            base.WordTableCell(content="Scale", formatter=formatters[0]),
            base.WordTableCell(content="Score", formatter=formatters[1]),
            base.WordTableCell(content="Clinical Relevance", formatter=formatters[2]),
        ]
        content_row = [
            base.WordTableCell(
                content="Social Communication Questionnaire", formatter=formatters[0]
            ),
            base.WordTableCell(
                content=f"{data.SCQ_Total:.0f}", formatter=formatters[1]
            ),
            base.WordTableCell(content=str(relevance), formatter=formatters[2]),
        ]

        return base.WordTableMarkup(rows=[header, content_row])


class ScqTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Scq table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Scq renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _ScqDataSource
