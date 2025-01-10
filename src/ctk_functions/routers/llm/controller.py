"""Controller for the LLM model."""

from ctk_functions.core import config
from ctk_functions.microservices import cloai_service

settings = config.get_settings()


async def run_llm(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Runs the model with the given prompts.

    Args:
        system_prompt: The system prompt to be used.
        user_prompt: The user prompt to be used.

    Returns:
        The output text.
    """
    client = cloai_service.Client()
    return await client.run(system_prompt, user_prompt)
