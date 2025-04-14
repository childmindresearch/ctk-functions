"""Module for inserting the academic achievement table."""

import dataclasses
import functools

import cmi_docx
from docx import shared
from docx.enum import text

from ctk_functions.microservices.sql import models
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
        subtest="TOWRE-2 Total Word Reading Efficiency",
        score_column="TOWRE_Total_S",
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
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("person_id", mrn, models.SummaryScores)
        header_formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        header = [
            base.WordTableCell(content="Domain", formatter=header_formatters[0]),
            base.WordTableCell(content="Subtest", formatter=header_formatters[1]),
            base.WordTableCell(
                content="Standard Score",
                formatter=header_formatters[2],
            ),
            base.WordTableCell(content="Percentile", formatter=header_formatters[3]),
            base.WordTableCell(content="Range", formatter=header_formatters[4]),
        ]

        body_formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        body_formatters[0].merge_top = True
        left_align = cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(
                alignment=text.WD_PARAGRAPH_ALIGNMENT.LEFT
            )
        )
        body_formatters[1].conditional_styles.append(
            base.ConditionalStyle(style=left_align)
        )
        content_rows = []
        for label in ACADEMIC_ROW_LABELS:
            score = getattr(data, label.score_column)
            if score is None:
                continue

            domain_cell = base.WordTableCell(
                content=label.domain,
                formatter=body_formatters[0],
            )
            subtest_cell = base.WordTableCell(
                content=label.subtest, formatter=body_formatters[1]
            )

            percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
            qualifier = utils.standard_score_to_qualifier(score)
            score_cell = base.WordTableCell(
                content=f"{score:.0f}", formatter=body_formatters[2]
            )
            percentile_cell = base.WordTableCell(
                content=f"{percentile:.0f}",
                formatter=body_formatters[3],
            )
            range_cell = base.WordTableCell(
                content=qualifier, formatter=body_formatters[4]
            )
            content_rows.append(
                (domain_cell, subtest_cell, score_cell, percentile_cell, range_cell),
            )

        return base.WordTableMarkup(
            rows=[header, *content_rows],
        )


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
