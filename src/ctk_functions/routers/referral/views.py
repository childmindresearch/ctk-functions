"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.referral import controller

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/referral")
def post_referral(
    table: tuple[tuple[str, ...], ...],
) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        table: The table to add to the referral report.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    docx_bytes = controller.post_referral(table)
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
