"""Contains dataclasses to build the introduction page."""

from collections.abc import Iterable
from typing import cast

import pydantic

from ctk_functions.core import config
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import sql_data, types
from ctk_functions.routers.pyrite.reports import sections

settings = config.get_settings()
DATA_DIR = settings.DATA_DIR


@pydantic.dataclasses.dataclass(frozen=True)
class TableColumn:
    """Stores the location of a column in a table."""

    model: type[models.Base]
    column: str


@pydantic.dataclasses.dataclass(frozen=True)
class TestOverview:
    """Definition of the introduction overview of a test."""

    id: types.TestId
    title: str
    description: str
    date_table: TableColumn | None


@pydantic.dataclasses.dataclass(frozen=True)
class TestOverviewManager:
    """Dataclass for all test descriptions."""

    def fetch(self, test_id: types.TestId) -> TestOverview | None:
        """Convenience method that mimics getattr with correct typing."""
        try:
            return cast("TestOverview", getattr(self, test_id))
        except AttributeError:
            return None

    cbcl = TestOverview(
        id="cbcl",
        title="Child Behavior Checklist - Parent Report Form (CBCL)",
        description="",
        date_table=None,
    )

    celf_5 = TestOverview(
        id="celf_5",
        title=(
            "Clinical Evaluation of Language Fundamentals - 5th Edition Screener "
            "(CELF-5 Screener)"
        ),
        description="",
        date_table=TableColumn(model=models.SummaryScores, column="CELF_Date"),
    )

    conners_3 = TestOverview(
        id="conners_3",
        title="Conners 3 Child Self-Report Assessment Form",
        description="",
        date_table=None,
    )

    ctopp_2 = TestOverview(
        id="ctopp_2",
        title="Comprehensive Test of Phonological Processing - 2nd Edition (CTOPP-2)",
        description="",
        date_table=TableColumn(model=models.SummaryScores, column="CTOPP_Date"),
    )

    grooved_pegboard = TestOverview(
        id="grooved_pegboard",
        title="Lafayette Grooved Pegboard Test",
        description="",
        date_table=None,
    )

    ksads = TestOverview(
        id="ksads",
        title="Kiddie Schedule for Affective Disorders and Schizophrenia (K-SADS)",
        description="",
        date_table=None,
    )

    mfq = TestOverview(
        id="mfq",
        title="Mood and Feelings Questionnaire (MFQ)",
        description="Child and Parent Report Forms",
        date_table=None,
    )

    scared = TestOverview(
        id="scared",
        title="Screen for Child Anxiety and Related Disorders (SCARED)",
        description="Child and Parent Report Forms",
        date_table=None,
    )

    srs = TestOverview(
        id="srs",
        title="Social Responsiveness Scale - 2 (SRS)",
        description="",
        date_table=None,
    )

    swan = TestOverview(
        id="swan",
        title=(
            "Extended Strengths and Weaknesses of ADHD Symptoms and Normal Behavior "
            "Scale (ESWAN)"
        ),
        description="",
        date_table=None,
    )

    towre_2 = TestOverview(
        id="towre_2",
        title="Test of Word Reading Efficiency-2nd Edition (TOWRE-2)",
        description="",
        date_table=TableColumn(model=models.SummaryScores, column="TOWRE_Date"),
    )

    wiat_4_essay = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Sentence Composition, Essay Composition",
        date_table=TableColumn(model=models.SummaryScores, column="WIAT_Writing_date"),
    )

    wiat_4_extended = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description=(
            "Reading Comprehension, Listening Comprehension, Math Problem Solving, "
            "Math Fluency Subtests"
        ),
        date_table=TableColumn(model=models.SummaryScores, column="WIAT_Part2_Date"),
    )

    wiat_4_screening = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Word Reading, Pseudoword Decoding, Spelling, Numerical Operations",
        date_table=TableColumn(model=models.SummaryScores, column="WIAT_Screen_Date"),
    )

    wisc_5 = TestOverview(
        id="wisc_5",
        title="Wechsler Intelligence Scale for Children, 5th Edition (WISC-V)",
        description=(
            "Vocabulary, Similarities, Block Design, Visual Puzzles, Matrix Reasoning, "
            "Figure Weights, Digit Span, Picture Memory, Coding, Symbol Search"
        ),
        date_table=TableColumn(model=models.SummaryScores, column="WISC_Date"),
    )


def test_ids_to_introduction(
    mrn: str, test_ids: Iterable[types.TestId]
) -> tuple[sections.Section, ...]:
    """Creates the introduction section of the report.

    Args:
        mrn: The participant's unique identifier.
        test_ids: The IDs of the tests to include.

    Returns:
        The introduction section of the report.
    """
    overviews = TestOverviewManager()
    used_overviews = [overviews.fetch(test_id) for test_id in test_ids]
    introduction_sections = [
        _overview_to_sections(mrn, overview) for overview in used_overviews if overview
    ]
    return (
        sections.ParagraphSection(
            content="STANDARDIZED TESTING, INTERVIEW AND QUESTIONNAIRE RESULTS",
            style="Heading 1",
        ),
        sections.ParagraphSection(
            content=(
                "This report provides a summary of the following tests, "
                "questionnaires, and clinical interviews that were administered during "
                "participation in the study. Areas assessed include general cognitive "
                "ability, academic achievement, language and fine motor coordination. "
                "Clinical interviews and questionnaires were used to assess social, "
                "emotional and behavioral functioning. Please reference Appendix A for "
                "a full description of the measures administered in the Healthy Brain "
                "Network research protocol."
            ),
            style=None,
        ),
        *introduction_sections,
        sections.PageBreak(),
        sections.ParagraphSection(
            content="What do the scores represent?",
            style="Heading 2",
        ),
        sections.ParagraphSection(
            content=(
                "Standard scores, T scores, and percentile ranks can indicate "
                "{{FIRST_NAME_POSSESSIVE}} performance compared to other children in "
                "the same age or same grade (see Figure below). A standard score of "
                "100 is the mean of the normative sample (individuals in the same age "
                "or same grade), and a standard score within the range of 90-109 "
                "indicates that an individual's performance or rating is within the "
                "average or typical range. A T score of 50 is the mean of the "
                "normative sample, and a T score within the range of 43-57 indicates "
                "that an individual's performance or ratings is within the average "
                "range. A percentile rank of 50 is the median of the normative sample, "
                "meaning that an individual's performance equals or exceeds 50% of the "
                "same-age peers. A percentile rank within the range of 25-75 indicates "
                "that an individual's performance or rating is within the average."
            ),
            style=None,
        ),
        sections.ImageSection(path=DATA_DIR / "pyrite_tscore_distribution.png"),
    )


def _overview_to_sections(mrn: str, overview: TestOverview) -> sections.Section:
    """Converts a test description to a section.

    Args:
        mrn: The participant's unique identifier.
        overview: The description of the test.

    Returns:
        The section for this test..
    """
    if overview.date_table:
        data = sql_data.fetch_participant_row(
            "person_id", mrn, overview.date_table.model
        )
        administer_date = str(getattr(data, overview.date_table.column))
    else:
        administer_date = ""

    if not overview.description:
        texts: tuple[str, ...] = (overview.title + "\n", "Administered on: ")
        run_styles: tuple[None | sections.RunStyles, ...] = (None, None)
    else:
        texts = (
            overview.title + "\n",
            overview.description + "\n",
            f"Administered on: {administer_date}",
        )
        run_styles = (None, sections.RunStyles.Emphasis, None)

    return sections.RunsSection(
        content=texts,
        paragraph_style="Normal Hanging",
        run_styles=run_styles,
    )
