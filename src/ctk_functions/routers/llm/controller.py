"""Controller for the LLM model."""

from ctk_functions.core import config
from ctk_functions.microservices import language_models

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
    client = language_models.get_llm(model)
    return await client.run(system_prompt, user_prompt)  # type: ignore[no-any-return] # I can't figure out why mypy believes this returns Any type.
