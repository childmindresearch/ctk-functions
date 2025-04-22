"""Module for inserting the academic achievement table."""

import dataclasses
import functools

import cmi_docx
from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import appendix_a
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(1.76),
    shared.Cm(7.24),
    shared.Cm(2.56),
    shared.Cm(2.2),
    shared.Cm(2.75),
)


@dataclasses.dataclass
class AcademicRowLabels:
    """Class definition for subtest rows.

    Attributes:
        domain: The domain of the WIAT subtest.
        subtest: Name of the subtest, used in second column.
        score_column: The label for standard score in the SQL data.
        style: Style to apply to this row.
    """

    domain: str
    subtest: str
    score_column: str
    style: base.ConditionalStyle | None = None


BOLD_STYLE = base.ConditionalStyle(
    style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True))
)

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
        subtest="TOWRE-2 Total Word Reading Efficiency",
        score_column="TOWRE_Total_S",
        style=base.Styles.BOLD,
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="\tSight Word Efficiency",
        score_column="TOWRE_SWE_S",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="\tPhonemic Decoding Efficiency",
        score_column="TOWRE_PDE_S",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Sentence Composition",
        score_column="WIAT_SComp_Std",
        style=base.Styles.BOLD,
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="\tSentence Building",
        score_column="WIAT_SB_Std",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="\tSentence Combining",
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
        style=base.Styles.BOLD,
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="\tMath Fluency - Addition",
        score_column="WIAT_MF_Add_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="\tMath Fluency - Subtraction",
        score_column="WIAT_MF_Sub_S",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="\tMath Fluency - Multiplication",
        score_column="WIAT_MF_Mult_S",
    ),
)


class _AcademicAchievementDataSource(base.DataProducer):
    """Fetches the data for the academic achievement table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[appendix_a.TestId, ...]:
        subtests = [row[1] for row in cls.fetch(mrn)]
        test_ids: list[appendix_a.TestId] = []
        if any("towre" in test.lower() for test in subtests):
            test_ids.append("towre_2")
        if any("wiat" in test.lower() for test in subtests):
            test_ids.append("wiat_4")
        return tuple(test_ids)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = utils.fetch_participant_row("person_id", mrn, models.SummaryScores)
        header = ("Domain", "Subtest", "Standard Score", "Percentile", "Range")
        body = []
        for label in ACADEMIC_ROW_LABELS:
            score = getattr(data, label.score_column)
            if score is None:
                continue

            percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
            qualifier = utils.standard_score_to_qualifier(score)
            body.append(
                (
                    label.domain,
                    label.subtest,
                    f"{score:.0f}",
                    f"{percentile:.0f}",
                    qualifier,
                ),
            )

        return header, *body


class AcademicAchievementTable(
    base.WordTableSectionAddToMixin,
    base.WordTableSection,
):
    """Renderer for the Academic Achievement composite table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Academic Achievement renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.preamble = [
            base.ParagraphBlock(content="Age Norms:"),
        ]
        self.data_source = _AcademicAchievementDataSource

        bold_subtests = [
            label.subtest
            for label in ACADEMIC_ROW_LABELS
            if label.style == base.Styles.BOLD
        ]
        with base.Styles.get("BOLD") as style:
            style.condition = lambda text: text in bold_subtests
            self.formatters = base.FormatProducer.produce(
                n_rows=len(self.data_source.fetch(mrn)),
                column_widths=COLUMN_WIDTHS,
                merge_top=(0,),
                column_styles={
                    1: (base.Styles.LEFT_ALIGN, style),
                },
            )
