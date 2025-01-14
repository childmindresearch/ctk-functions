"""Controller for service health."""

import asyncio

import aiohttp

from ctk_functions.core import config
from ctk_functions.routers.health import schemas

settings = config.get_settings()
LANGUAGE_TOOL_URL = settings.LANGUAGE_TOOL_URL
CLOAI_SERVICE_URL = settings.CLOAI_SERVICE_URL


async def get_health() -> schemas.GetHealthResponse:
    """Gets the health of connected services."""
    async with aiohttp.ClientSession() as session:
        llm_promise = session.get(CLOAI_SERVICE_URL + "/health")
        language_tool_promise = session.get(LANGUAGE_TOOL_URL + "/languages")

        llm_response, language_tool_response = await asyncio.gather(
            llm_promise,
            language_tool_promise,
        )

    return schemas.GetHealthResponse(
        cloai_service=llm_response.ok,
        language_tool=language_tool_response.ok,
    )
