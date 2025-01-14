"""Endpoint definitions for the health endpoints."""

import fastapi

from ctk_functions.routers.health import controller, schemas

router = fastapi.APIRouter(prefix="/health", tags=["health"])


@router.get(path="")
async def health_endpoint() -> schemas.GetHealthResponse:
    """Health check endpoint."""
    return await controller.get_health()
