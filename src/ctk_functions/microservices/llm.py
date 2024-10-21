"""This module coalesces all large language models from different microservices."""

import asyncio
import inspect
import json
import typing
from collections.abc import Iterable
from typing import Literal, TypeGuard, overload

import instructor
import pydantic

from ctk_functions import config
from ctk_functions.microservices import aws, azure, utils

settings = config.get_settings()
LOGGER_PHI_LOGGING_LEVEL = settings.LOGGER_PHI_LOGGING_LEVEL
VALID_LLM_MODELS = typing.Literal[aws.ANTHROPIC_MODELS, azure.GPT_MODELS]
logger = config.get_logger()


class GeneratedQuestion(pydantic.BaseModel):
    """A class for a question to be asked about the correctness of an LLM result."""

    question: str = pydantic.Field(
        ...,
        description="A True or False question about the text.",
    )

    @pydantic.field_validator("question")
    @classmethod
    def question_ends_in_question_mark(cls, value: str) -> str:
        """Check whether the phrase is actually a question."""
        if not value.endswith("?"):
            msg = "Questions must end with a question mark."
            raise ValueError(msg)
        return value


class VerificationQuestion(pydantic.BaseModel):
    """A class for a question verifying the correctness of an LLM result."""

    question: str = pydantic.Field(
        ...,
        description="A True or False question about the text.",
    )
    correct: bool = pydantic.Field(
        ...,
        description="True if the answer to the question is true, False otherwise.",
    )

    @pydantic.field_validator("question")
    @classmethod
    def question_ends_in_question_mark(cls, value: str) -> str:
        """Check whether the phrase is actually a question."""
        if not value.endswith("?"):
            msg = "Questions must end with a question mark."
            raise ValueError(msg)
        return value


class LargeLanguageModel(utils.LlmAbstractBaseClass):
    """Llm class that provides access to all available LLMs.

    Attributes:
        client: The client for the large language model.
    """

    def __init__(self, model: VALID_LLM_MODELS) -> None:
        """Initializes the language model.

        Args:
            model: The model to use for the language model.
        """
        self.client: azure.AzureLlm | aws.ClaudeLlm
        self.instructor: (
            instructor.client.Instructor | instructor.client.AsyncInstructor
        )
        self.model = model
        logger.info("Using LLM model: %s", self.model)
        if self._is_azure_model(self.model):
            self.client = azure.AzureLlm(self.model)
            self.instructor = instructor.from_openai(self.client.client)
        elif self._is_aws_model(self.model):
            self.client = aws.ClaudeLlm(self.model)
            self.instructor = instructor.from_anthropic(self.client.client)
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
        return await self.client.run(system_prompt, user_prompt)

    @overload
    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        questions: list[str] = ...,
        max_verifications: int = ...,
        *,
        create_new_questions: bool,
    ) -> str:
        pass

    @overload
    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        questions: None = None,
        max_verifications: int = ...,
        *,
        create_new_questions: Literal[True],
    ) -> str:
        pass

    async def chain_of_verification(
        self,
        system_prompt: str,
        user_prompt: str,
        questions: list[str] | None = None,
        max_verifications: int = 3,
        *,
        create_new_questions: bool = False,
    ) -> str:
        """Runs an LLM prompt that is self-assessed by the LLM.

        Args:
            system_prompt: The system prompt for the initial prompt.
            user_prompt: The user prompt for the initial prompt.
            questions: Questions to verify the results. Defaults to None.
            max_verifications: The maximum number of times to verify the results.
                Defaults to 3.
            create_new_questions: If True, generate new questions from the system
                prompt. Defaults to False.

        Returns:
            The editted text result.
        """
        if questions is None and not create_new_questions:
            msg = (
                "Either questions must be provided, or new questions need to be "
                "generated, or both."
            )
            raise ValueError(msg)
        questions = questions or []

        text_promise = self.client.run(system_prompt, user_prompt)
        if create_new_questions:
            questions_promise = self._create_questions(system_prompt)
            text, new_questions = await asyncio.gather(text_promise, questions_promise)
            questions += new_questions
        else:
            text = await text_promise

        logger.log(
            LOGGER_PHI_LOGGING_LEVEL,
            "Running with questions: %s",
            questions,
        )
        for _ in range(max_verifications):
            logger.log(LOGGER_PHI_LOGGING_LEVEL, text)
            verified_questions = await self._verify_questions(
                text,
                questions,
            )
            if all(question.correct for question in verified_questions):
                break
            logger.log(
                LOGGER_PHI_LOGGING_LEVEL,
                [q for q in verified_questions if not q.correct],
            )
            text = await self._rewrite(text, verified_questions, user_prompt)
        else:
            logger.warning("Reached verification limit.")

        return text

    async def _create_questions(self, instructions: str) -> list[str]:
        """Creates questions for prompt result validation.

        Args:
            instructions: The instructions provided to the model, commonly
                the system prompt.

        Returns:
            List of verification questions as strings.
        """
        system_message = (
            "Based on the following instructions, write a set questions that can be "
            "answered with True or False to determine whether a piece of text adheres "
            "to these instructions."
        )
        messages = [
            {
                "role": "user",
                "content": instructions,
            },
        ]

        response = self.instructor.chat.completions.create(
            list[str],
            messages,  # type: ignore[arg-type]
            system=system_message,
            model=self.model,
            max_tokens=4096,
        )

        if inspect.isawaitable(response):
            response = await response

        return response

    async def _verify_questions(
        self,
        text: str,
        questions: Iterable[str],
    ) -> list[VerificationQuestion]:
        system_prompt = (
            "Assess whether all of the following questions about the text "
            "are True or False: {}"
        ).format("\n".join(questions))
        response = self.instructor.chat.completions.create(
            response_model=list[VerificationQuestion],
            system=system_prompt,
            messages=[{"role": "user", "content": text}],
            model=self.model,
            max_tokens=4096,
        )

        if inspect.isawaitable(response):
            response = await response

        return response

    async def _rewrite(
        self,
        text: str,
        questions: Iterable[VerificationQuestion],
        source: str,
    ) -> str:
        system_prompt = (
            "Based on the responses to the following questions, "
            "rewrite the text to ensure that all questions are True: "
            "\n".join(json.dumps(question.model_dump()) for question in questions)
            + "Ensure that everything stated in the text is accurate with respect to "
            f"the source material. The source material is as follows: \n\n {source}"
        )

        return await self.client.run(system_prompt, text)

    @staticmethod
    def _is_azure_model(model: VALID_LLM_MODELS) -> TypeGuard[azure.GPT_MODELS]:
        return model in typing.get_args(azure.GPT_MODELS)

    @staticmethod
    def _is_aws_model(model: VALID_LLM_MODELS) -> TypeGuard[aws.ANTHROPIC_MODELS]:
        return model in typing.get_args(aws.ANTHROPIC_MODELS)
