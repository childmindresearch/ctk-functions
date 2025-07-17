"""Functions for converting files between different formats."""

from ctk_functions.core import config
from ctk_functions.microservices import language_tool
from ctk_functions.routers.language_tool import schemas

settings = config.get_settings()


async def run_language_tool(body: schemas.PostLanguageToolRequest) -> str:
    """Corrects the grammar of the input text.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        The corrected text.
    """
    async with language_tool.LanguageCorrecter(
        body.rules,
        settings.LANGUAGE_TOOL_URL,
    ) as correcter:
        return await correcter.correct(body.text)
