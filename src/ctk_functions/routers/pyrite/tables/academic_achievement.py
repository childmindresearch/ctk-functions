"""Module for inserting the academic achievement table."""

import dataclasses
import functools

from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class AcademicRowLabels:
    """Class definition for subtest rows.

    Attributes:
        domain: The domain of the WIAT subtest.
        subtest: Name of the subtest, used in second column.
        score_column: The label for standard score in the SQL data.
    """

    domain: str
    subtest: str
    score_column: str


# Defines the rows and their order of appearance.
ACADEMIC_ROW_LABELS = (
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Word Reading",
        score_column="WIAT_Word_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Pseudoword Decoding",
        score_column="WIAT_Pseudo_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Reading Comprehension",
        score_column="WIAT_Read_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Total Word Reading Efficiency",
        score_column="TOWRE_Total_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Sight Word Efficiency",
        score_column="TOWRE_SWE_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Phonemic Decoding Efficiency",
        score_column="TOWRE_PDE_S",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Sentence Composition",
        score_column="WIAT_SComp_Std",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="Sentence Building",
        score_column="WIAT_SB_Std",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="Sentence Combining",
        score_column="WIAT_SC_Std",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Essay Composition",
        score_column="WIAT_EC_Std",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Spelling",
        score_column="WIAT_Spell_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Numerical Operations",
        score_column="WIAT_Num_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Math Problem Solving",
        score_column="WIAT_Math_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Math Fluency",
        score_column="WIAT_MF_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Addition",
        score_column="WIAT_MF_Add_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Subtraction",
        score_column="WIAT_MF_Sub_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Multiplication",
        score_column="WIAT_MF_Mult_S",
    ),
)


class AcademicAchievementDataSource(base.DataProducer):
    """Fetches the data for the academic achievement table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("person_id", mrn, models.SummaryScores)

        header = [
            base.WordTableCell(content="Domain"),
            base.WordTableCell(content="Subtest"),
            base.WordTableCell(content="Standard Score"),
            base.WordTableCell(content="Percentile"),
            base.WordTableCell(content="Range"),
        ]
        content_rows = []
        for label in ACADEMIC_ROW_LABELS:
            domain_cell = base.WordTableCell(
                content=label.domain,
                formatter=base.Formatter(merge_top=True),
            )
            subtest_cell = base.WordTableCell(content=label.subtest)

            score = getattr(data, label.score_column)
            if score is None:
                n_a_cell = base.WordTableCell(content="N/A")
                content_rows.append(
                    (domain_cell, subtest_cell, n_a_cell, n_a_cell, n_a_cell),
                )
                continue

            percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
            qualifier = utils.standard_score_to_qualifier(score)
            score_cell = base.WordTableCell(content=f"{score:.0f}")
            percentile_cell = base.WordTableCell(content=f"{percentile:.0f}")
            range_cell = base.WordTableCell(content=qualifier)
            content_rows.append(
                (domain_cell, subtest_cell, score_cell, percentile_cell, range_cell),
            )

        return base.WordTableMarkup(rows=[header, *content_rows])


class AcademicAchievementTable(
    base.WordTableSection,
    data_source=AcademicAchievementDataSource,
):
    """Renderer for the Academic Achievement composite table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Academic Achievement renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.preamble = [
            base.ParagraphBlock(
                content="Academic Achievement",
                level=utils.TABLE_TITLE_LEVEL,
            ),
            base.ParagraphBlock(content="Age Norms:"),
        ]

    def add_to(self, doc: document.Document) -> None:
        """Adds the Academic Achievement table to the document."""
        markup = self.data_source.fetch(self.mrn)
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        renderer = base.WordDocumentTableSectionRenderer(
            preamble=self.preamble,
            table_renderer=table_renderer,
        )
        renderer.add_to(doc)
