"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.referral import controller, schemas

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/referral")
def post_referral(
    request: schemas.PostReferralRequest,
) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        request: The table to add to the referral report.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    docx_bytes = controller.post_referral(request)
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
