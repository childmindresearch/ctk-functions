"""Module for inserting the academic achievement table."""

import dataclasses
from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class RowLabels:
    """Class definition for subtest rows.

    Attributes:
        domain: The domain of the WIAT subtest.
        subtest: Name of the subtest, used in second column.
        score: The label for standard score in the SQL data.
        percentile: The label for percentile in the SQL data.
    """

    domain: str
    subtest: str
    score: str
    percentile: str


# Defines the rows and their order of appearance.
ROW_LABELS = (
    RowLabels(
        domain="Reading",
        subtest="WIAT-4 Word Reading",
        score="WIAT_Word_Stnd",
        percentile="WIAT_Word_P",
    ),
    RowLabels(
        domain="Reading",
        subtest="WIAT-4 Pseudoword Decoding",
        score="WIAT_Pseudo_Stnd",
        percentile="WIAT_Pseudo_P",
    ),
    RowLabels(
        domain="Reading",
        subtest="WIAT-4 Reading Comprehension",
        score="WIAT_RC_Stnd",
        percentile="WIAT_RC_P",
    ),
    RowLabels(
        domain="Reading",
        subtest="TOWRE-II Total Word Reading Efficiency",
        score="TOWRE_Total_Scaled",
        percentile="TOWRE_Total_Perc",
    ),
    RowLabels(
        domain="Reading",
        subtest="TOWRE-II Sight Word Efficiency",
        score="TOWRE_SWE_Scaled",
        percentile="TOWRE_SWE_Perc",
    ),
    RowLabels(
        domain="Reading",
        subtest="TOWRE-II Phonemic Decoding Efficiency",
        score="TOWRE_PDE_Scaled",
        percentile="TOWRE_PDE_Perc",
    ),
    RowLabels(
        domain="Writing",
        subtest="WIAT-4 Sentence Composition",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Writing",
        subtest="Sentence Building",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Writing",
        subtest="Sentence Combining",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Writing",
        subtest="WIAT-4 Essay Composition",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Writing",
        subtest="WIAT-4 Spelling",
        score="WIAT_Spell_Stnd",
        percentile="WIAT_Spell_P",
    ),
    RowLabels(
        domain="Math",
        subtest="WIAT-4 Numerical Operations",
        score="WIAT_Num_Stnd",
        percentile="WIAT_Num_P",
    ),
    RowLabels(
        domain="Math",
        subtest="WIAT-4 Math Problem Solving",
        score="WIAT_MP_Stnd",
        percentile="WIAT_MP_P",
    ),
    RowLabels(
        domain="Math",
        subtest="WIAT-4 Math Fluency",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Math",
        subtest="Math Fluency - Addition",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Math",
        subtest="Math Fluency - Subtraction",
        score="XXX",
        percentile="XXX",
    ),
    RowLabels(
        domain="Math",
        subtest="Math Fluency - Multiplication",
        score="XXX",
        percentile="XXX",
    ),
)


class AcademicAchievement(base.BaseTable):
    """Fetches and creates the academic achievement table."""

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return (
            sqlalchemy.select(
                models.t_I2B2_Export_WIAT_t,
                models.t_I2B2_Export_TOWRE_t,
            )
            .where(
                self.eid == models.t_I2B2_Export_WIAT_t.c.EID,  # type: ignore[arg-type]
            )
            .outerjoin(
                models.t_I2B2_Export_TOWRE_t,
                models.t_I2B2_Export_WIAT_t.c.EID == models.t_I2B2_Export_TOWRE_t.c.EID,
            )
        )

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds academic achievement table to document.

        Args:
            doc: The Word document.
        """
        doc.add_paragraph("Age Norms:")
        header_texts = [
            "Domain",
            "Subtest",
            "Standard Score",
            "Percentile",
            "Range",
        ]
        table = doc.add_table(1 + len(ROW_LABELS), len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(ROW_LABELS):
            index += 1  # Offset for the header row.  # noqa: PLW2901
            utils.set_index_column_name_or_merge(table, label.domain, index)
            row = table.rows[index].cells
            row[1].text = label.subtest
            if label.score == "XXX":
                continue
            score = int(getattr(self._data_no_none, label.score))
            percentile = utils.standard_score_to_percentile(score)
            row[2].text = str(score)
            row[3].text = str(percentile)
            row[4].text = utils.standard_score_to_qualifier(score)
