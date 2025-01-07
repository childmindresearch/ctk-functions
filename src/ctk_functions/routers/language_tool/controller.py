"""Functions for converting files between different formats."""

from ctk_functions.core import config
from ctk_functions.routers.language_tool import schemas
from ctk_functions.text import corrections

settings = config.get_settings()


async def language_tool(body: schemas.PostLanguageToolRequest) -> str:
    """Corrects the grammar of the input text.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        The corrected text.
    """
    correcter = corrections.LanguageCorrecter(body.rules, settings.LANGUAGE_TOOL_URL)
    return await correcter.correct(body.text)
