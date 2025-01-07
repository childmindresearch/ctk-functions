"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.language_tool import controller, schemas

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/language-tool")
async def post_language_tool(body: schemas.PostLanguageToolRequest) -> str:
    """POST endpoint for markdown2docx.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    return await controller.language_tool(body)
