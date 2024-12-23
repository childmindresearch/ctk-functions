"""Controller for the LLM model."""

from ctk_functions.core import config
from ctk_functions.microservices import llm
from ctk_functions.routers.llm import schemas

settings = config.get_settings()


async def run_llm(body: schemas.PostLlmRequest) -> str:
    """Runs the model with the given prompts.

    Args:
        body: The request body, see schemas for full description.

    Returns:
        The output text.
    """
    return await llm.LargeLanguageModel(model=body.model).run(
        body.system_prompt,
        body.user_prompt,
    )
