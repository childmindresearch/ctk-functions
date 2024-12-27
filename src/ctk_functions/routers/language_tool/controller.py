"""Functions for converting files between different formats."""

from ctk_functions.routers.language_tool import schemas
from ctk_functions.text import corrections


def language_tool(body: schemas.PostLanguageToolRequest) -> str:
    """Corrects the grammar of the input text.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        The corrected text.
    """
    correcter = corrections.LanguageCorrecter(body.rules)
    return correcter.run(body.text)
