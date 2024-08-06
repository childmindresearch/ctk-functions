"""Functions for converting files between different formats."""

from ctk_functions.text import corrections


async def language_tool(text: str, rules: list[str] = []) -> str:
    """Corrects the grammar of the input text.

    Args:
        text: The text to correct.
        rules: The rules to enable.

    Returns:
        The corrected text.
    """
    correcter = corrections.LanguageCorrecter(rules)
    return await correcter.run(text)
