"""Unit tests for the writer module."""

import dataclasses
import datetime
from typing import Literal

import docx
import pytest

from ctk_functions.routers.intake.intake_processing import writer


@dataclasses.dataclass
class Language:
    """Basic replacement for parser.Language."""

    name: str
    fluency: Literal["fluent", "proficient", "conversational", "basic"]


@dataclasses.dataclass
class MockGuardian:
    """Basic replacement for parser.GuardianInformation."""

    title_name: str = "Mr. Lukas Fink"


@dataclasses.dataclass
class MockPatient:
    """Basic replacement for parser.PatientInformation."""

    full_name: str = "Lea Avatar"
    first_name: str = "Lea"
    date_of_birth: datetime.datetime = datetime.datetime(
        2015,
        1,
        1,
        tzinfo=datetime.UTC,
    )
    guardian: MockGuardian = dataclasses.field(default_factory=MockGuardian)
    age_gender_label: str = "girl"
    pronouns: list[str] = dataclasses.field(
        default_factory=lambda: ["she", "her", "her", "hers", "herself"],
    )


@dataclasses.dataclass
class MockIntake:
    """Basic replacement for parser.IntakeInformation."""

    patient: MockPatient = dataclasses.field(default_factory=MockPatient)
    date_of_intake: str = "03/03/2023"


def test_replace_patient_information() -> None:
    """Test that the method returns correctly formatted text."""
    intake = MockIntake()
    document = docx.Document()
    paragraph = document.add_paragraph("{{FULL_NAME}} is a {{PRONOUN_0}}.")
    paragraph.add_run(" {{PRONOUN_2}}")
    report_writer = writer.ReportWriter(intake, "gpt-4o")  # type: ignore[arg-type]
    report_writer.report.document = document
    expected = "Lea Avatar is a she. her"

    report_writer.replace_patient_information()
    actual = report_writer.report.document.paragraphs[0].text

    assert actual == expected


@pytest.mark.parametrize(
    ("languages", "expected"),
    [
        ([], ""),
        ([Language("English", "fluent")], "is fluent in English"),
        (
            [Language("English", "fluent"), Language("Spanish", "proficient")],
            "is fluent in English and proficient in Spanish",
        ),
        (
            [
                Language("English", "fluent"),
                Language("Spanish", "proficient"),
                Language("French", "conversational"),
            ],
            "is fluent in English, proficient in Spanish, and conversational in French",
        ),
        (
            [
                Language("English", "fluent"),
                Language("Spanish", "proficient"),
                Language("French", "conversational"),
                Language("German", "basic"),
            ],
            (
                "is fluent in English, proficient in Spanish, conversational in "
                "French, and has basic skills in German"
            ),
        ),
        (
            [
                Language("English", "fluent"),
                Language("Spanish", "fluent"),
                Language("French", "conversational"),
            ],
            "is fluent in English and Spanish and conversational in French",
        ),
        (
            [
                Language("English", "fluent"),
                Language("Spanish", "fluent"),
                Language("French", "fluent"),
            ],
            "is fluent in English, Spanish, and French",
        ),
    ],
)
def test__join_patient_languages(languages: Language, expected: str) -> None:
    """Test that the _join_patient_languages method returns correctly formatted text."""
    actual = writer.ReportWriter._join_patient_languages(languages)  # type: ignore[arg-type] # Tested in test_valid_language_replacement.

    assert actual == expected


def test_set_superscript() -> None:
    """Test that the set_superscript method returns correctly formatted text."""
    intake = MockIntake()
    report = writer.ReportWriter(intake, "gpt-4o")  # type: ignore[arg-type]
    document = docx.Document()
    document.add_paragraph("For the 1st time.")
    report.report.document = document

    report.set_superscripts()

    assert document.paragraphs[0].text == "For the 1st time."
    assert document.paragraphs[0].runs[0].text == "For the 1"
    assert document.paragraphs[0].runs[1].text == "st"
    assert document.paragraphs[0].runs[2].text == " time."
    assert document.paragraphs[0].runs[1].font.superscript
