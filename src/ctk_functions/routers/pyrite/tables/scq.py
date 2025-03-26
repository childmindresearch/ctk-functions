"""Module for fetching the Social Communication Questionnaire data."""

import cmi_docx
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


class ScqDataSource(base.DataProducer):
    """Fetches and creates the SCQ table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the Scq data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.Scq)
        relevance = base.ClinicalRelevance(
            low=10,
            high=None,
            label="Evidence of clinical concern of ASD",
            style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0))),
        )
        formatter = base.Formatter(
            conditional_styles=[
                base.ConditionalStyle(
                    condition=relevance.in_range,
                    style=relevance.style,
                ),
            ],
        )
        header = [
            base.WordTableCell(content="Scale"),
            base.WordTableCell(content="Score"),
            base.WordTableCell(content="Clinical Relevance"),
        ]
        content_row = [
            base.WordTableCell(content="Social Communication Questionnaire"),
            base.WordTableCell(content=f"{data.SCQ_Total:.0f}", formatter=formatter),
            base.WordTableCell(content=str(relevance)),
        ]

        return base.WordTableMarkup(rows=[header, content_row])


class ScqTable(base.WordTableSection):
    """Renderer for the Scq table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Scq renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = ScqDataSource().fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content="Social Communication Questionnaire",
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the Scq table to the document."""
        self.renderer.add_to(doc)
