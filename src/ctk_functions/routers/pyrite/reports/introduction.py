from typing import cast

import pydantic

from ctk_functions.routers.pyrite.reports import utils


@pydantic.dataclasses.dataclass(frozen=True)
class TestOverview:
    """Definition of the introduction overview of a test."""

    id: utils.TestId
    title: str
    description: str
    administered_on: None = None  # TODO


@pydantic.dataclasses.dataclass(frozen=True)
class TestOverviewManager:
    """Dataclass for all test descriptions."""

    def fetch(self, test_id: utils.TestId) -> TestOverview | None:
        """Convenience method that mimics getattr with correct typing."""
        try:
            return cast("TestOverview", getattr(self, test_id))
        except AttributeError:
            return None

    cbcl = TestOverview(
        id="cbcl",
        title="Child Behavior Checklist - Parent Report Form (CBCL)",
        description="",
    )

    celf_5 = TestOverview(
        id="celf_5",
        title="Clinical Evaluation of Language Fundamentals - 5th Edition Screener (CELF-5 Screener)",
        description="",
    )

    conners_3 = TestOverview(
        id="conners_3",
        title="Conners 3 Child Self-Report Assessment Form",
        description="",
    )
    ctopp_2 = TestOverview(
        id="ctopp_2",
        title="Comprehensive Test of Phonological Processing - 2nd Edition (CTOPP-2)",
        description="",
    )

    ksads = TestOverview(
        id="ksads",
        title="Kiddie Schedule for Affective Disorders and Schizophrenia (K-SADS)",
        description="",
    )

    mfq = TestOverview(
        id="mfq",
        title="Mood and Feelings Questionnaire (MFQ)",
        description="Child and Parent Report Forms",
    )
    scared = TestOverview(
        id="scared",
        title="Screen for Child Anxiety and Related Disorders (SCARED)",
        description="Child and Parent Report Forms",
    )
    srs = TestOverview(
        id="srs",
        title="Social Responsiveness Scale - 2 (SRS)",
        description="",
    )

    swan = TestOverview(
        id="swan",
        title="Extended Strengths and Weaknesses of ADHD Symptoms and Normal Behavior Scale (ESWAN)",
        description="",
    )

    towre_2 = TestOverview(
        id="towre_2",
        title="Test of Word Reading Efficiency-2nd Edition (TOWRE-2)",
        description="",
    )

    wiat_4_essay = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Sentence Composition, Essay Composition",
    )

    wiat_4_extended = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Reading Comprehension, Listening Comprehension, Math Problem Solving, Math Fluency Subtests",
    )
    wiat_4_screening = TestOverview(
        id="wiat_4",
        title="Wechsler Individual Achievement Test, 4th Edition (WIAT-4)",
        description="Word Reading, Pseudoword Decoding, Spelling, Numerical Operations",
    )

    wisc_5 = TestOverview(
        id="wisc_5",
        title="Wechsler Intelligence Scale for Children, 5th Edition (WISC-V)",
        description=(
            "Vocabulary, Similarities, Block Design, Visual Puzzles, Matrix Reasoning, "
            "Figure Weights, Digit Span, Picture Memory, Coding, Symbol Search"
        ),
    )
