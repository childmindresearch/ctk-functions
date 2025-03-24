"""Module for inserting the Conners3 table."""

import dataclasses

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, tscore


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
    """

    name: str
    column: str


CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=57,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=57,
        high=63,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=63,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]

# Defines the rows and their order of appearance.
CONNERS3_ROW_LABELS = (
    tscore.TScoreRowLabel(
        subscale="Inattention",
        score_column="C3SR_IN_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Hyperactivity/Impulsivity",
        score_column="C3SR_HY_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Learning Problems",
        score_column="C3SR_LP_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Defiance/Aggression",
        score_column="C3SR_AG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    tscore.TScoreRowLabel(
        subscale="Family Relations",
        score_column="C3SR_FR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class Conners3(base.BaseTable):
    """Fetches and creates the Conners3 table."""

    def add(self, doc: document.Document) -> None:
        """Adds the Conners3 table to the document.

        Args:
            doc: The document to add the Conners3 table to.
        """
        data_source: base.SqlDataSource[models.Conners3] = base.SqlDataSource(
            query=sqlalchemy.select(models.Conners3).where(
                models.Conners3.EID == self.eid,
            ),
        )

        tbl = tscore.build_tscore_table(
            data_source,
            CONNERS3_ROW_LABELS,
            title="Social Responsiveness Scale",
        )
        tbl.add(doc)
