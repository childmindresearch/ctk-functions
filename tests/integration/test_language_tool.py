"""Tests the language tool."""

from ctk_functions.microservices import language_tool


def test_lanugage_correcter() -> None:
    """Tests the language correcter."""
    correcter = language_tool.LanguageCorrecter()
    text = "They is good."

    corrections = correcter.check(text)

    assert len(corrections) == 1
    assert corrections[0].rule.id == "PERS_PRONOUN_AGREEMENT"
