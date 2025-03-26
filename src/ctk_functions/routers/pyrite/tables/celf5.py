"""Gets the data for the CELF-5 Table."""

from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


class Celf5DataSource(base.DataProducer):
    """Fetches the data for the Celf5 table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the Celf5 data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.Celf5)
        markup = [
            [
                base.WordTableCell(content="Test"),
                base.WordTableCell(content="Total Score"),
                base.WordTableCell(content="Age Based Cutoff"),
                base.WordTableCell(content="Range"),
            ],
            [
                base.WordTableCell(content="CELF-5 Screener"),
                base.WordTableCell(content=f"{data.CELF_Total:.0f}"),
                base.WordTableCell(content=f"{data.CELF_CriterionScore:.0f}"),
                base.WordTableCell(
                    content="Meets criterion cutoff"
                    if data.CELF_ExceedCutoff
                    else "Does not meet criterion cutoff",
                ),
            ],
        ]

        return base.WordTableMarkup(rows=markup)


class Celf5Table(base.WordTableSection):
    """Renderer for the CELF5 table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the CELF5 renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = Celf5DataSource().fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content="Language Screening",
                level=utils.TABLE_TITLE_LEVEL,
            ),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the CELF5 table to the document."""
        self.renderer.add_to(doc)
