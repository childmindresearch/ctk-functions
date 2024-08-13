"""Functions for converting files between different formats."""

from ctk_functions.text import corrections


def language_tool(text: str, rules: list[str] | None = None) -> str:
    """Corrects the grammar of the input text.

    Args:
        text: The text to correct.
        rules: The rules to enable.

    Returns:
        The corrected text.
    """
    if rules is None:
        rules = []
    correcter = corrections.LanguageCorrecter(rules)
    return correcter.run(text)
