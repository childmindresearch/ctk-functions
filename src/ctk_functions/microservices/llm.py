"""This module coalesces all large language models from different microservices."""

import asyncio
import typing
from collections.abc import Iterable
from typing import Any, Literal, TypeGuard, TypeVar, overload

import instructor
import pydantic

from ctk_functions import config
from ctk_functions.microservices import aws, azure, utils

settings = config.get_settings()
LOGGER_PHI_LOGGING_LEVEL = settings.LOGGER_PHI_LOGGING_LEVEL
VALID_LLM_MODELS = typing.Literal[aws.ANTHROPIC_MODELS, azure.GPT_MODELS]
logger = config.get_logger()

T = TypeVar("T")


class GeneratedStatement(pydantic.BaseModel):
    """A class for a statement about the correctness of an LLM result."""

    statement: str = pydantic.Field(
        ...,
        description="A True or False statement about the text.",
    )

    @pydantic.field_validator("statement")
    @classmethod
    def statement_validation(cls, value: str) -> str:
        """Check whether the phrase is actually a statement."""
        if value[0].isnumeric():
            msg = "statements should not be numbered."
            raise ValueError(msg)
        return value


class VerificationStatement(pydantic.BaseModel):
    """A class for a statement verifying the correctness of an LLM result."""

    statement: GeneratedStatement = pydantic.Field(
        ...,
        description="A True or False statement about the text.",
    )
    correct: bool = pydantic.Field(
        ...,
        description="True if the answer to the statement is true, False otherwise.",
    )


class RewrittenText(pydantic.BaseModel):
    """Class for rewriting text based on verification statements."""

    text: str = pydantic.Field(..., description="The editted text.")
    statements: tuple[VerificationStatement] = pydantic.Field(
        ...,
        description=(
            "The statements along with whether they are True or False about the "
            "editted text."
        ),
    )


class LargeLanguageModel(pydantic.BaseModel, utils.LlmAbstractBaseClass):
    """Llm class that provides access to all available LLMs.

    Attributes:
        client: The client for the large language model.
    """

    model: VALID_LLM_MODELS
    _client: azure.AzureLlm | aws.ClaudeLlm = pydantic.PrivateAttr()
    _instructor_client: instructor.client.AsyncInstructor = pydantic.PrivateAttr()

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, __context: Any) -> None:  # noqa: ANN401
        """Initializes the language model.

        Args:
            model: The model to use for the language model.
        """
        logger.info("Using LLM model: %s", self.model)
        if self._is_azure_model(self.model):
            self._client = azure.AzureLlm(self.model)
            self._instructor_client = instructor.from_openai(self._client.client)
        elif self._is_aws_model(self.model):
            self._client = aws.ClaudeLlm(self.model)
            self._instructor_client = instructor.from_anthropic(self._client.client)
        else:
            # As the model name can be supplied by the user, this case might be reached.
            msg = f"Invalid LLM model: {self.model}"
            raise ValueError(msg)

    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        return await self._client.run(system_prompt, user_prompt)

    @overload
    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        statements: list[str] = ...,
        max_verifications: int = ...,
        *,
        create_new_statements: bool,
    ) -> str:
        pass

    @overload
    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        statements: None = None,
        max_verifications: int = ...,
        *,
        create_new_statements: Literal[True],
    ) -> str:
        pass

    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        statements: list[str] | None = None,
        max_verifications: int = 3,
        *,
        create_new_statements: bool = False,
    ) -> str:
        """Runs an LLM prompt that is self-assessed by the LLM.

        Args:
            system_prompt: The system prompt for the initial prompt.
            user_prompt: The user prompt for the initial prompt.
            statements: Statements to verify the results. Defaults to None.
            max_verifications: The maximum number of times to verify the results.
                Defaults to 3.
            create_new_statements: If True, generate new statements from the system
                prompt. Defaults to False.

        Returns:
            The editted text result.
        """
        if statements is None and not create_new_statements:
            msg = (
                "Either statements must be provided, or new statements need to be "
                "generated, or both."
            )
            raise ValueError(msg)
        statements = statements or []

        text_promise = self.run(system_prompt, user_prompt)
        if create_new_statements:
            statements_promise = self._create_statements(system_prompt)
            text, new_statements = await asyncio.gather(
                text_promise,
                statements_promise,
            )
            statements += [statement.statement for statement in new_statements]
        else:
            text = await text_promise

        logger.log(
            LOGGER_PHI_LOGGING_LEVEL,
            "Running with statements: %s",
            statements,
        )
        for _ in range(max_verifications):
            logger.log(LOGGER_PHI_LOGGING_LEVEL, text)
            rewrite = await self._verify(
                text,
                statements,
                user_prompt,
            )
            if all(statement.correct for statement in rewrite.statements):
                break
            logger.log(
                LOGGER_PHI_LOGGING_LEVEL,
                [q for q in rewrite.statements if not q.correct],
            )
            text = rewrite.text
        else:
            logger.warning("Reached verification limit.")

        return text

    async def _create_statements(self, instructions: str) -> list[GeneratedStatement]:
        """Creates statements for prompt result validation.

        Args:
            instructions: The instructions provided to the model, commonly
                the system prompt.

        Returns:
            List of verification statements as strings.
        """
        system_prompt = """
Based on the following instructions, write a set of statements that can be
answered with True or False to determine whether a piece of text adheres to
these instructions. True should denote adherence to the structure whereas
False should denote a lack of adherence.
            """

        return await self.call_instructor(
            list[GeneratedStatement],
            system_prompt=system_prompt,
            user_prompt=instructions,
            max_tokens=4096,
        )

    async def call_instructor(
        self,
        response_model: type[T],
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
    ) -> T:
        """Generic interface for Anthropic/OpenAI instructor."""
        if self._is_aws_model(self.model):
            return await self._instructor_client.chat.completions.create(  # type: ignore[type-var]
                response_model=response_model,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                system=system_prompt,
                model=self.model,
                max_tokens=max_tokens,
            )
        if self._is_azure_model(self.model):
            return await self._instructor_client.chat.completions.create(  # type: ignore[type-var]
                response_model=response_model,
                messages=[
                    {
                        "role": "system",
                        "content": user_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                model=self.model,
                max_tokens=max_tokens,
            )
        msg = "Invalid model."
        raise ValueError(msg)

    async def _verify(
        self,
        text: str,
        statements: Iterable[str],
        source: str,
    ) -> RewrittenText:
        statement_string = "\n".join(statements)
        system_prompt = (
            "Based on the following statements, edit the text to comply"
            f"with all statements. The statements are as follows: "
            f"{statement_string}. Furthermore, ensure that all edits are reflective "
            f"of the source material: {source}"
        )
        return await self.call_instructor(
            response_model=RewrittenText,
            system_prompt=system_prompt,
            user_prompt=text,
            max_tokens=4096,
        )

    @staticmethod
    def _is_azure_model(model: VALID_LLM_MODELS) -> TypeGuard[azure.GPT_MODELS]:
        return model in typing.get_args(azure.GPT_MODELS)

    @staticmethod
    def _is_aws_model(model: VALID_LLM_MODELS) -> TypeGuard[aws.ANTHROPIC_MODELS]:
        return model in typing.get_args(aws.ANTHROPIC_MODELS)
