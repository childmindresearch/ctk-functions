"""Tests for the text corrections module."""

import pytest

from ctk_functions.text import corrections


@pytest.fixture(scope="module")
def correcter() -> corrections.LanguageCorrecter:
    """Fixture for the LanguageCorrecter class.

    The initialization is slow, so it is performed at the module level.
    """
    return corrections.LanguageCorrecter(
        url="http://0.0.0.0:8010/v2",
        enabled_rules=[
            "PERS_PRONOUN_AGREEMENT",
            "UPPERCASE_SENTENCE_START",
            "NON3PRS_VERB",
            "COMMA_COMPOUND_SENTENCE_2",
        ],
    )


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ("They is going to the store.", "They are going to the store."),
        ("they is going to the store.", "They are going to the store."),
        (
            "He is going to the store. they are walking the dog.",
            "He is going to the store. They are walking the dog.",
        ),
        ("The store to which they has gone.", "The store to which they have gone."),
        (
            (
                "A very long sentence because the context is clipped when the sentence"
                " is too long but the results should still be correct. They is going"
                " to the store."
            ),
            (
                "A very long sentence because the context is clipped when the sentence"
                " is too long, but the results should still be correct. They are going"
                " to the store."
            ),
        ),
        ("", ""),
    ],
)
@pytest.mark.asyncio
async def test_text_corrections(
    correcter: corrections.LanguageCorrecter,
    input_text: str,
    expected: str,
) -> None:
    """Tests the entrypoint of the TextCorrections class."""
    actual = await correcter.correct(input_text)

    assert actual == expected
