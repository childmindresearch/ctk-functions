"""Unit tests for the writer module."""

import dataclasses
from typing import Literal

import pytest

from ctk_functions.intake import descriptors, parser, writer


@dataclasses.dataclass
class Language:
    """Basic replacement for parser.Language."""

    name: str
    fluency: Literal["fluent", "proficient", "conversational", "basic"]


def test_valid_language_replacement() -> None:
    """Sanity check to test that the language replacement is valid."""
    patient_data = {
        "child_language1": "Dutch",
        "child_language1_fluency": 4,
        "child_language1_spoken": "yes",
        "child_language1_age": "1 year",
        "child_language1_setting": "home",
    }

    parser_language = parser.Language(patient_data, identifier=1)
    test_language = Language(
        patient_data["child_language1"],  # type: ignore[arg-type]
        descriptors.LanguageFluency(patient_data["child_language1_fluency"]).name,  # type: ignore[arg-type]
    )

    assert parser_language.name == test_language.name
    assert parser_language.fluency == test_language.fluency


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
