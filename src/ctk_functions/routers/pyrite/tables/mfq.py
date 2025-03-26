"""Module for getting the Mood and Feelings Questionnaire table."""

import cmi_docx
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils
from ctk_functions.routers.pyrite.tables.generic import parent_child

MFQ_ROW_LABELS = (
    parent_child.ParentChildRow(
        subscale="Total Score",
        parent_column="MFQ_P_Total",
        child_column="MFQ_SR_Total",
        relevance=[
            base.ClinicalRelevance(
                low=None,
                high=26,
                label=None,
                high_inclusive=False,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
)


class MfqDataSource(base.DataProducer):
    """Fetches the data for the MFQ table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the MFQ data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        return parent_child.build_parent_child_table(
            mrn,
            models.MfqParent,
            models.MfqSelf,
            MFQ_ROW_LABELS,
        )


class MfqTable(base.WordTableSection):
    """Renderer for the Mfq table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Mfq renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = MfqDataSource().fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content="Mood and Feelings Questionnaire (MFQ) - Long Version",
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the Mfq table to the document."""
        self.renderer.add_to(doc)
