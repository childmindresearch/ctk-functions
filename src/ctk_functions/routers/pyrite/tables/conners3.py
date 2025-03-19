"""Module for inserting the Conners3 table."""

import dataclasses
from typing import Any

import cmi_docx
import sqlalchemy

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        column: Column name, used for accessing the SQL data.
    """

    name: str
    column: str


CLINICAL_RELEVANCE = (
    utils.ClinicalRelevance(
        low=None,
        high=57,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=57,
        high=63,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=63,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)

# Defines the rows and their order of appearance.
ROW_LABELS = (
    base.TScoreRow(
        name="Inattention",
        column="C3SR_IN_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Hyperactivity/Impulsivity",
        column="C3SR_HY_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Learning Problems",
        column="C3SR_LP_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Defiance/Aggression",
        column="C3SR_AG_T",
        relevance=CLINICAL_RELEVANCE,
    ),
    base.TScoreRow(
        name="Family Relations",
        column="C3SR_FR_T",
        relevance=CLINICAL_RELEVANCE,
    ),
)


class Conners3(base.TScoreTable):
    """Fetches and creates the Conners3 table."""

    _title = "Conners 3 - Child Short Form"
    _row_labels = ROW_LABELS

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_C3SR_t).where(
            self.eid == models.t_I2B2_Export_C3SR_t.c.EID,  # type: ignore[arg-type]
        )
