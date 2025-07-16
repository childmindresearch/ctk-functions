"""Tests for the intake writer module."""

import pytest

from ctk_functions.routers.intake.intake_processing.utils import (
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
    assert string_utils.oxford_comma(elements) == expected


def test_join_with_oxford_comma_join_word() -> None:
    """Tests joining a list with an Oxford comma and a join word."""
    expected = "a, b, or c"

    actual = string_utils.oxford_comma(["a", "b", "c"], join_word="or")

    assert actual == expected


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
