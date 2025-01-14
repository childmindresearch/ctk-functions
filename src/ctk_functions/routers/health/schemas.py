"""Schemas for health endpoints."""

import pydantic


class GetHealthResponse(pydantic.BaseModel):
    """Health of connected services."""

    cloai_service: bool
    language_tool: bool
