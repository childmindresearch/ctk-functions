"""Controller for the LLM model."""

from ctk_functions import config
from ctk_functions.microservices import llm

settings = config.get_settings()


async def run_llm(
    model: llm.VALID_LLM_MODELS,
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Runs the model with the given prompts.

    Args:
        model: The model to use for the language model.
        system_prompt: The system prompt.
        user_prompt: The user prompt.

    Returns:
        The output text.
    """
    return await llm.LargeLanguageModel(model=model).run(system_prompt, user_prompt)
