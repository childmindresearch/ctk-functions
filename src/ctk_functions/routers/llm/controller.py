"""Controller for the LLM model."""

from ctk_functions.core import config
from ctk_functions.microservices import llm

settings = config.get_settings()


async def run_llm(
    model: str,
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Runs the model with the given prompts.

    Args:
        model: The model to run.
        system_prompt: The system prompt to be used.
        user_prompt: The user prompt to be used.

    Returns:
        The output text.
    """
    return await llm.get_llm(model).run(
        system_prompt,
        user_prompt,
    )
