"""Controller for the LLM model."""

from ctk_functions import config
from ctk_functions.microservices import aws

settings = config.get_settings()
LLM_MODEL = settings.LLM_MODEL


def run_llm(system_prompt: str, user_prompt: str) -> str:
    """Runs the model with the given prompts.

    Args:
        system_prompt: The system prompt.
        user_prompt: The user prompt.

    Returns:
        The output text.
    """
    bedrock_llm = aws.BedRockLlm(model=LLM_MODEL, region_name="us-east-1")
    return bedrock_llm.run(system_prompt, user_prompt)
