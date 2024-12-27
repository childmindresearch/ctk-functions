"""Large Language Model client creation."""

from typing import Literal, TypeGuard, get_args

import cloai
from cloai.llm import bedrock

from ctk_functions.core import config

settings = config.get_settings()

VALID_MODELS = Literal[
    "anthropic.claude-3-opus-20240229-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "gpt-4o",
]


def get_llm(model: str) -> cloai.LargeLanguageModel:
    """Gets the LLM client.

    Args:
        model: Model name to use.

    Returns:
        The client for the large language model.
    """
    if _is_anthropic_bedrock_model(model):
        client = cloai.AnthropicBedrockLlm(
            model=model,
            aws_access_key=settings.AWS_ACCESS_KEY_ID.get_secret_value(),
            aws_secret_key=settings.AWS_SECRET_ACCESS_KEY.get_secret_value(),
            region=settings.AWS_REGION,
        )
    else:
        client = cloai.AzureLlm(
            deployment=settings.AZURE_OPENAI_LLM_DEPLOYMENT.get_secret_value(),
            endpoint=settings.AZURE_OPENAI_ENDPOINT.get_secret_value(),
            api_key=settings.AZURE_OPENAI_API_KEY.get_secret_value(),
            api_version="2024-02-01",
        )
    return cloai.LargeLanguageModel(client=client)


def _is_anthropic_bedrock_model(
    model: str,
) -> TypeGuard[bedrock.ANTHROPIC_BEDROCK_MODELS]:
    return model in get_args(bedrock.ANTHROPIC_BEDROCK_MODELS)
