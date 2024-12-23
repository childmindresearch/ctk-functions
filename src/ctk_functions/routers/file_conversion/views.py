"""Endpoints for the file conversion router."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.file_conversion import controller, schemas

logger = config.get_logger()
router = fastapi.APIRouter(prefix="")


@router.post("/markdown2docx")
def markdown2docx(body: schemas.PostMarkdown2DocxRequest) -> fastapi.Response:
    """POST endpoint for markdown2docx.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        A FastAPI response containing the bytes of a .docx file.
    """
    logger.info("Converting Markdown to .docx")
    docx_bytes = controller.markdown2docx(
        markdown=body.markdown,
        formatting=body.formatting,
    )
    return fastapi.Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
