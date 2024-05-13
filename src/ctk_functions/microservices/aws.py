"""This module contains interactions with AWS microservices."""

import asyncio
import json

import boto3
import botocore

config = botocore.config.Config(retries={"max_attempts": 100, "mode": "standard"})


class BedRockLlm:
    """A class to interact with the BedRock service."""

    def __init__(self, model: str, region_name: str) -> None:
        """Initializes the BedRock client."""
        self.client = boto3.client(
            "bedrock-runtime", region_name=region_name, config=config
        )
        self.model = model

    def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        prompt = f"[INST]{system_prompt}\n{user_prompt}[/INST]"
        body = json.dumps(
            {
                "prompt": prompt,
                "temperature": 0.5,
                "top_p": 0.9,
            }
        )
        response = self.client.invoke_model(
            body=body,
            modelId=self.model,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        return response_body["outputs"][0]["text"]

    async def run_async(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts asynchronously.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        return await asyncio.to_thread(self.run, system_prompt, user_prompt)
