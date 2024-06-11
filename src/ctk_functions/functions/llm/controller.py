"""Controller for the LLM model."""

from ctk_functions import config
from ctk_functions.microservices import azure

settings = config.get_settings()


async def run_llm(system_prompt: str, user_prompt: str) -> str:
    """Runs the model with the given prompts.

    Args:
        system_prompt: The system prompt.
        user_prompt: The user prompt.

    Returns:
        The output text.
    """
    llm = azure.AzureLlm()
    return await llm.run(system_prompt, user_prompt)
