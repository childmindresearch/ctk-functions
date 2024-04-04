"""Tests for the intake writer module."""

import pytest

from ctk_functions.intake.utils import (
    language_utils,
    string_utils,
)


@pytest.mark.parametrize(
    ("elements", "expected"),
    [
        ([], ""),
        (["a"], "a"),
        (["a", "b"], "a and b"),
        (["a", "b", "c"], "a, b, and c"),
        (["a", "b", "c", "d"], "a, b, c, and d"),
    ],
)
def test_join_with_oxford_comma(elements: list[str], expected: str) -> None:
    """Tests joining a list with an Oxford comma."""
    assert string_utils.join_with_oxford_comma(elements) == expected


@pytest.mark.parametrize(
    ("rank", "suffix"),
    [
        (-1, "th"),
        (0, "th"),
        (1, "st"),
        (2, "nd"),
        (3, "rd"),
        (4, "th"),
        (11, "th"),
        (12, "th"),
        (13, "th"),
        (14, "th"),
        (21, "st"),
        (22, "nd"),
        (23, "rd"),
        (24, "th"),
        (1111, "th"),
        ("1", "st"),
    ],
)
def test_ordinal_suffix(rank: int, suffix: str) -> None:
    """Tests getting the ordinal suffix of a number."""
    assert string_utils.ordinal_suffix(rank) == suffix


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("They hears it in your voice.", "They hear it in your voice."),
        ('She hears it in your voice."', "She hears it in your voice."),
        (
            "They has been waiting from sprinkler splashes until fireplace ashes.",
            "They have been waiting from sprinkler splashes until fireplace ashes.",
        ),
        (
            "She has been waiting from sprinkler splashes until fireplace ashes.",
            "She has been waiting from sprinkler splashes until fireplace ashes.",
        ),
    ],
)
def correct_verb_conjugation(sentence: str, expected: str) -> None:
    """Tests whether the verb conjugations of they are corrected."""
    obj = language_utils.DocumentCorrections(document="")
    pairs = obj._find_subject_verb(sentence)

    for pair in pairs:
        sentence = obj._correct_they_verb_conjugation(
            sentence,
            pair,
        )

    assert sentence == expected


def test_remove_excess_whitespace() -> None:
    """Test the _remove_excess_whitespace method."""
    test_text = """    This   is a test string with

    excess    whitespace.     """
    expected = "This is a test string with excess whitespace."

    actual = string_utils.remove_excess_whitespace(test_text)

    assert actual == expected


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("1", 1),
        ("1st", 1),
        ("1 month", 1),
        ("1.5", 1.5),
        ("1.5 months", 1.5),
        ("twenty five", 25),
        ("5 months and 4 days", "5 months and 4 days"),
    ],
)
def test_string_to_int(string: str, expected: float) -> None:
    """Test the string_to_int method."""
    actual = string_utils.StringToInt().parse(string)

    assert actual == expected
    assert isinstance(actual, type(expected))
