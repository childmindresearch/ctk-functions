"""Endpoints for the file conversion router."""

from typing import Annotated

import fastapi

from ctk_functions.core import config
from ctk_functions.microservices import llm
from ctk_functions.routers.intake import controller

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.get("/intake-report/{mrn}")
async def post_language_tool(
    mrn: str,
    x_model: Annotated[llm.VALID_LLM_MODELS, fastapi.Header()],
) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        mrn: The identifier of the participant. If it starts with 'mock', will
            use the mock participant.
        x_model: The name of the LLM to use.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    docx_bytes = await controller.get_intake_report(mrn, x_model)
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
