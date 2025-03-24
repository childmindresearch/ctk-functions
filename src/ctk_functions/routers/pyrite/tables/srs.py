"""Definition of the Social Responsiveness Scale table."""

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, tscore

CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=75,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=75,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


# Defines the rows and their order of appearance.
SRS_ROW_LABELS = (
    tscore.TScoreRowLabel(
        subscale="Social Awareness",
        score_column="SRS_AWR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Cognition",
        score_column="SRS_COG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Communication",
        score_column="SRS_COM_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Social Motivation",
        score_column="SRS_MOT_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Restrictive and Repetitive Behavior",
        score_column="SRS_RRB_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Total Score",
        score_column="SRS_Total_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class Srs(base.PyriteBaseTable):
    """Generates a table displaying Social Responsiveness Scale results."""

    def add(self, doc: document.Document) -> None:
        """Add the SRS table to the provided document.

        Args:
            doc: The Word document to which the table will be added.
        """
        data_source: base.SqlDataSource[models.Srs] = base.SqlDataSource(
            query=sqlalchemy.select(models.Srs).where(models.Srs.EID == self.eid),
        )

        tbl = tscore.build_tscore_table(
            data_source,
            SRS_ROW_LABELS,
            title="Social Responsiveness Scale",
        )
        tbl.add(doc)
