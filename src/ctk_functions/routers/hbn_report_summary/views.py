"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.hbn_report_summary import controller, schemas

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/report-summary")
async def post_report_summary(
    body: schemas.PostReportSummaryRequest,
) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    docx_bytes = await controller.report_summary(
        user_prompt=body.user_prompt,
    )
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
