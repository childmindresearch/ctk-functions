"""Contains dataclasses to build the introduction page."""

from collections.abc import Generator, Iterable

import pydantic

from ctk_functions.core import config
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import sql_data, types
from ctk_functions.routers.pyrite.reports import sections

settings = config.get_settings()
DATA_DIR = settings.DATA_DIR


@pydantic.dataclasses.dataclass(frozen=True)
class SqlTableColumn:
    """Stores the location of a column in a table.

    The WIAT table requires a fallback option, hence columns
    is an iterable.

    Args:
        model: The model to fetch data from.
        columns: List of columns to use in order of priority i.e.
            data from the first non-null column is used.
    """

    model: type[models.Base]
    columns: tuple[str, ...]


@pydantic.dataclasses.dataclass(frozen=True)
class TestOverview:
    """Definition of the introduction overview of a test."""

    id: types.TestId
    title: str
    description: str
    date_table: SqlTableColumn | None


class TestOverviewManager(pydantic.BaseModel):
    """Dataclass for all test descriptions."""

    cbcl: TestOverview = TestOverview(
        id="cbcl",
        title="Child Behavior Checklist - Parent Report Form (CBCL)",
        description="",
        date_table=None,
    )

    celf_5: TestOverview = TestOverview(
        id="celf_5",
        title=(
            "Clinical Evaluation of Language Fundamentals - 5th Edition Screener "
            "(CELF-5 Screener)"
        ),
        description="",
        date_table=SqlTableColumn(model=models.SummaryScores, columns=("CELF_Date",)),
    )

    conners_3: TestOverview = TestOverview(
        id="conners_3",
        title="Conners 3 Child Self-Report Assessment Form",
        description="",
        date_table=None,
    )

    ctopp_2: TestOverview = TestOverview(
        id="ctopp_2",
        title="Comprehensive Test of Phonological Processing - 2nd Edition (CTOPP-2)",
        description="",
        date_table=SqlTableColumn(model=models.SummaryScores, columns=("CTOPP_Date",)),
    )

    grooved_pegboard: TestOverview = TestOverview(
        id="grooved_pegboard",
        title="Lafayette Grooved Pegboard Test",
        description="",
        date_table=SqlTableColumn(
            model=models.SummaryScores, columns=("Pegboard_Date",)
        ),
    )

    ksads: TestOverview = TestOverview(
        id="ksads",
        title="Kiddie Schedule for Affective Disorders and Schizophrenia (K-SADS)",
        description="",
        date_table=None,
    )

    mfq: TestOverview = TestOverview(
        id="mfq",
        title="Mood and Feelings Questionnaire (MFQ)",
        description="Child and Parent Report Forms",
        date_table=None,
    )

    scared: TestOverview = TestOverview(
        id="scared",
        title="Screen for Child Anxiety and Related Disorders (SCARED)",
        description="Child and Parent Report Forms",
        date_table=None,
    )

    srs: TestOverview = TestOverview(
        id="srs",
        title="Social Responsiveness Scale - 2 (SRS)",
        description="",
        date_table=None,
    )

    swan: TestOverview = TestOverview(
        id="swan",
        title=(
            "Extended Strengths and Weaknesses of ADHD Symptoms and Normal Behavior "
            "Scale (ESWAN)"
        ),
        description="",
        date_table=None,
    )

    towre_2: TestOverview = TestOverview(
        id="towre_2",
        title="Test of Word Reading Efficiency-2nd Edition (TOWRE-2)",
        description="",
        date_table=SqlTableColumn(model=models.SummaryScores, columns=("TOWRE_Date",)),
    )

    wiat_4_essay: TestOverview = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Sentence Composition, Essay Composition",
        date_table=SqlTableColumn(
            model=models.SummaryScores, columns=("WIAT_Writing_date", "WIAT_Date")
        ),
    )

    wiat_4_extended: TestOverview = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description=(
            "Reading Comprehension, Listening Comprehension, Math Problem Solving, "
            "Math Fluency Subtests"
        ),
        date_table=SqlTableColumn(
            model=models.SummaryScores, columns=("WIAT_Part2_Date", "WIAT_Date")
        ),
    )

    wiat_4_screening: TestOverview = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Word Reading, Pseudoword Decoding, Spelling, Numerical Operations",
        date_table=SqlTableColumn(
            model=models.SummaryScores, columns=("WIAT_Screen_Date", "WIAT_Date")
        ),
    )

    wisc_5: TestOverview = TestOverview(
        id="wisc_5",
        title="Wechsler Intelligence Scale for Children, 5th Edition (WISC-V)",
        description=(
            "Vocabulary, Similarities, Block Design, Visual Puzzles, Matrix Reasoning, "
            "Figure Weights, Digit Span, Picture Memory, Coding, Symbol Search"
        ),
        date_table=SqlTableColumn(model=models.SummaryScores, columns=("WISC_Date",)),
    )


def _fetch_overviews(test_id: types.TestId) -> Generator[TestOverview, None, None]:
    """Convenience method that gets all tests with an ID."""
    overviews = TestOverviewManager()
    for _, value in overviews:
        if value.id == test_id:
            yield value


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
    used_overviews = [
        overview for test_id in test_ids for overview in _fetch_overviews(test_id)
    ]
    introduction_sections = [
        _overview_to_sections(mrn, overview) for overview in used_overviews
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
        test_date = next(
            (
                getattr(data, col)
                for col in overview.date_table.columns
                if getattr(data, col)
            ),
            None,
        )
    else:
        test_date = None
    administer_date = f"Administered on: {test_date if test_date else 'UNKNOWN'}"

    if not overview.description:
        texts: tuple[str, ...] = (overview.title + "\n", administer_date)
        run_styles: tuple[None | sections.RunStyles, ...] = (None, None)
    else:
        texts = (
            overview.title + "\n",
            overview.description + "\n",
            administer_date,
        )
        run_styles = (None, sections.RunStyles.Emphasis, None)

    return sections.RunsSection(
        content=texts,
        paragraph_style="Normal Hanging",
        run_styles=run_styles,
    )
