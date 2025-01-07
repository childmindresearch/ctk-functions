"""Middleware for the API server."""

from collections.abc import Awaitable, Callable

import fastapi
from starlette.middleware import base

from ctk_functions.core import config

logger = config.get_logger()


class LoggingMiddleware(base.BaseHTTPMiddleware):
    """Logs requests and the status of their responses."""

    async def dispatch(
        self,
        request: fastapi.Request,
        call_next: Callable[[fastapi.Request], Awaitable[fastapi.Response]],
    ) -> fastapi.Response:
        """Logs the incoming requests and returns the response.

        Args:
            request: The incoming request.
            call_next: The function to call the request with.
        '
        """
        user = _sanitize_user_input(request.headers.get("X-User", "unknown"))
        request_id = _sanitize_user_input(
            request.headers.get("X-Request-Id", "unknown"),
        )
        endpoint = _sanitize_user_input(request.url.path)
        logger.debug(
            "Start request %s from user %s targeting %s",
            request_id,
            user,
            endpoint,
        )
        response = await call_next(request)
        logger.debug(
            "Finish request %s from user %s targeting %s with status %s.",
            request_id,
            user,
            endpoint,
            response.status_code,
        )
        return response


def _sanitize_user_input(user_input: str) -> str:
    """Ensures that logged user input matches some basic requirements.

    Performs the following operations:
    1. Removes leading/trailing whitespace.
    2. Limits the total number of characters to 50.
    3. Removes everything after a first new line character, including that character.

    Args:
        user_input: The user input to sanitize.

    Returns:
        The sanitized user input.
    """
    return user_input.strip()[:50].split("\n")[0]
