"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.intake import controller

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.get("/intake-report/{mrn}")
async def post_intake_report(
    mrn: str,
) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        mrn: The identifier of the participant. If it starts with 'mock', will
            use the mock participant.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    docx_bytes = await controller.get_intake_report(mrn)
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
