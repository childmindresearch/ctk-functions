"""Interactions with Large Language Models via cloai-service."""

from typing import TypeVar

import aiohttp
import fastapi
import pydantic
from fastapi import status

from ctk_functions.core import config

T = TypeVar("T", bound=pydantic.BaseModel)

settings = config.get_settings()
CLOAI_SERVICE_URL = settings.CLOAI_SERVICE_URL
CLOAI_MODEL = settings.CLOAI_MODEL

logger = config.get_logger()


class Client:
    """Client for interactions with cloai-service."""

    def __init__(self) -> None:
        """Initializes the cloai-service client."""
        self.url = CLOAI_SERVICE_URL
        self.model = CLOAI_MODEL

    async def run(self, user_prompt: str, system_prompt: str) -> str:
        """Runs a regular LLM call.

        Args:
            user_prompt: The user's message.
            system_prompt: The system's message.
        """
        async with aiohttp.request(
            "post",
            url=f"{self.url}/llm/run?id={self.model}",
            json={
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            },
        ) as response:
            if response.ok:
                return str((await response.json())["result"])
            text = await response.text()
            logger.error(text)
            raise fastapi.HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                text,
            )

    async def call_instructor(
        self,
        model: type[T],
        user_prompt: str,
        system_prompt: str,
    ) -> T:
        """Runs a call to instructor.

        Args:
            model: The requested model to return, must inherit from pydantic.BaseModel.
            user_prompt: The user's message.
            system_prompt: The system's message.
        """
        async with aiohttp.request(
            "post",
            url=f"{self.url}/llm/instructor?id={self.model}",
            json={
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "response_model": model.model_json_schema(),
            },
        ) as response:
            if response.ok:
                data = (await response.json())["result"]
                return model(**data)
            text = await response.text()
            logger.error(text)
            raise fastapi.HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                text,
            )

    async def chain_of_verification(
        self,
        user_prompt: str,
        system_prompt: str,
    ) -> str:
        """Runs a chain of verification.

        Args:
            user_prompt: The user's message.
            system_prompt: The system's message.
        """
        async with aiohttp.request(
            "post",
            url=f"{self.url}/llm/cov?id={self.model}",
            json={
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "create_new_statements": True,
            },
        ) as response:
            if response.ok:
                return str((await response.json())["result"])
            text = await response.text()
            logger.error(text)
            raise fastapi.HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                text,
            )
