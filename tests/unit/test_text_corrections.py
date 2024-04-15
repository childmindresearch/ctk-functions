"""Tests for the text corrections module."""

import pytest

from ctk_functions.text import corrections


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("They is going to the store.", "They are going to the store."),
        ("they is going to the store.", "They are going to the store."),
        (
            "He is going to the store.\nThey is walking the dog.",
            "He is going to the store.\nThey are walking the dog.",
        ),
        (
            "He is going to the store. they are walking the dog.",
            "He is going to the store. They are walking the dog.",
        ),
    ],
)
def test_text_corrections(input_text: str, expected: str) -> None:
    """Tests the entrypoint of the TextCorrections class."""
    correcter = corrections.TextCorrections(
        correct_they=True, correct_capitalization=True
    )

    actual = correcter.correct(input_text)

    assert actual == expected


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ("", ""),
        ("a", "A"),
        ("a b c", "A b c"),
        (" a B C", " A B C"),
    ],
)
def test_correct_capitalization(input_text: str, expected: str) -> None:
    """Tests the capitalization correction."""
    correcter = corrections.TextCorrections(
        correct_they=False, correct_capitalization=True
    )

    actual = correcter._correct_capitalization(input_text)

    assert actual == expected
