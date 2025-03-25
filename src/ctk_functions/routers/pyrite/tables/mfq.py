"""Module for getting the Mood and Feelings Questionnaire table."""

import cmi_docx

from ctk_functions.microservices.sql import models
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
