"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.llm import controller, schemas

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/llm")
async def post_llm(body: schemas.PostLlmRequest) -> str:
    """POST endpoint for markdown2docx.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    return await controller.run_llm(
        system_prompt=body.system_prompt,
        user_prompt=body.user_prompt,
    )
