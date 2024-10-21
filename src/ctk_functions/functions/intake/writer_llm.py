"""Large language model functionality for the intake module."""

import dataclasses
import uuid
from collections.abc import Awaitable, Sequence
from typing import Any

import jsonpickle

from ctk_functions import config
from ctk_functions.functions.intake.utils import string_utils
from ctk_functions.microservices import llm

logger = config.get_logger()
settings = config.get_settings()

LOGGER_PHI_LOGGING_LEVEL = settings.LOGGER_PHI_LOGGING_LEVEL


@dataclasses.dataclass
class LlmPlaceholder:
    """Represents a placeholder for large language model input in the report.

    Attributes:
        id: The unique identifier for the placeholder.
        replacement: The replacement text for the placeholder. Provided as
            an awaitable to allow for asynchronous processing.
    """

    id: str
    replacement: Awaitable[str]


@dataclasses.dataclass
class Prompts:
    """Prompts for the large language model."""

    parent_input = """
You will receive an excerpt of a clinical report with part of the text replaced
by a placeholder, a response by a parent, and the name and pronouns of the
child. Your task is to insert the parent's response into the excerpt. You should
return the excerpt in full with the placeholder replaced by the parent's
response. Do not use quotations; make sure the response is
integrated into the text. If the response is not provided, please write that the
response was not provided. If the response is not applicable, please write that
the information is not applicable. Parents' responses may be terse,
grammatically incorrect, or incomplete. Make sure that the response is clear,
uses correct grammar, avoids abbreviations and repetition, and is consistent
with the tone of a clinical report written by a medical professional.  Report
dates in the format "Month YYYY" (e.g., June 2022). Do not include an initial
message in the response like "Based on the parent input provided here is a
suggested completion" or a header like "Excerpt:" or "Parent Input"; INCLUDE
ONLY THE EXCERPT ITSELF.
"""
    edit = """
You will receive an excerpt of a clinical report. Your task is to edit the text
to improve its clarity, grammar, and style. You should return the excerpt in
full with the necessary edits. Ensure that the tone is appropriate for a
clinical report written by a doctor, i.e. professional and objective. Do not use
quotations; make sure the response is integrated into the text. Do not alter the
content of the text; ONLY EDIT THE TEXT FOR CLARITY, GRAMMAR, AND STYLE. Make sure
that the response is clear, uses correct grammar, avoids abbreviations and
repetition, and is consistent with the tone of a clinical report written by a
medical professional. Report dates in the format "Month YYYY" (e.g., June 2022).
Do not include any headers like "Excerpt" or "Here is the editted text". Format
your response as plaintext.
"""
    object_input = """
You will receive a JSON containing information about the patient. Your task is to write
a text that includes the clinically relevant information from the JSON. You
should return the text in full with the necessary edits. Make sure that the text
flows naturally, i.e., DO NOT MAKE A BULLET LIST. Format the text as plaintext.

This text will be inserted into a clinical report. Ensure that the tone is
appropriate for a clinical report written by a doctor, i.e. professional and
objective. Do not use quotations; make sure the response is integrated into the
text. Your response should be in plain text i.e., do not use Markdown. Do not
include an introduction, summary, or conclusion. Report dates in the format "Month YYYY"
(e.g., June 2022).
"""


class WriterLlm:
    """Class to represent the interface to a large language model.

    Each run_* method will return a placeholder that can be inserted into the
    report. All placeholders as well as their replacements will be stored in the
    placeholders attribute. The replacements are awaitables to allow for
    asynchronous processing.

    Attributes:
        client: The client to use for the language model.
        child_name: The name of the child in the report.
        child_pronouns: The pronouns of the child in the report.
        placeholders: The placeholders and their replacements.
    """

    def __init__(
        self,
        model: llm.VALID_LLM_MODELS,
        child_name: str,
        child_pronouns: Sequence[str],
    ) -> None:
        """Initializes the language model.

        Args:
            model: The model to use for the language model.
            child_name: The name of the child in the report.
            child_pronouns: The pronouns of the child in the report.
        """
        self.client = llm.LargeLanguageModel(model)
        self.child_name = child_name
        self.child_pronouns = child_pronouns
        self.placeholders: list[LlmPlaceholder] = []

    def run_text_with_parent_input(
        self,
        text: str,
        parent_input: str,
        additional_instruction: str = "",
        context: str = "",
    ) -> str:
        """Creates a placeholder for an LLM edit of an excerpt with parent input.

        Args:
            text: The excerpt to edit.
            parent_input: The parent input to insert into the excerpt.
            additional_instruction: Additional instructions to include in the system
                prompt.
            context: The context in which the excerpt will be placed.

        Returns:
            The placeholder for the LLM edit.
        """
        user_prompt = f"""
            Excerpt: {text}.
            Parent Input: {parent_input}.
        """
        additional_instruction = string_utils.remove_excess_whitespace(
            additional_instruction,
        )
        context = string_utils.remove_excess_whitespace(context)

        user_prompt = string_utils.remove_excess_whitespace(user_prompt)
        system_prompt = (
            f"{Prompts.parent_input}\n\n{self.child_info}\n\n{additional_instruction}"
        )
        if context:
            instruction = (
                "The following is the context preceding where the excerpt will be "
                "placed, do not include this context in your response:"
            )
            system_prompt = f"{system_prompt} {instruction} {context}\n\n"

        return self._run(system_prompt, user_prompt)

    def run_edit(
        self,
        text: str,
        additional_instruction: str = "",
        context: str = "",
        *,
        verify: bool = False,
    ) -> str:
        """Creates a placeholder for an LLM edit of an excerpt.

        Args:
            text: The excerpt to edit.
            additional_instruction: Additional instructions to include in the system
                prompt.
            context: The context in which the excerpt will be placed.
            verify: If true, run verification prompts on the LLM output.

        Returns:
            The placeholder for the LLM edit.
        """
        additional_instruction = string_utils.remove_excess_whitespace(
            additional_instruction,
        )
        context = string_utils.remove_excess_whitespace(context)
        user_prompt = string_utils.remove_excess_whitespace(text)

        system_prompt = f"{Prompts.edit}\n{additional_instruction}"
        if context:
            instruction = (
                "The following is the context preceding where the excerpt will be "
                "placed, do not include this context in your response:"
            )
            system_prompt = f"{system_prompt} {instruction} {context}\n\n"
        return self._run(system_prompt, user_prompt, verify=verify)

    def run_with_object_input(
        self,
        items: Any,  # noqa: ANN401
        additional_instruction: str = "",
        *,
        verify: bool = False,
    ) -> str:
        """Creates a placeholder for an LLM edit of a list of classes.

        Args:
            items: An object which will be converted to JSON.
            additional_instruction: Additional instructions to include in the system
                prompt.
            verify: If true, run verification prompts on the LLM output.

        Returns:
            The placeholder for the LLM edit.
        """
        additional_instruction = string_utils.remove_excess_whitespace(
            additional_instruction,
        )

        system_prompt = (
            f"{Prompts.object_input}\n{self.child_info}\n{additional_instruction}"
        )
        user_prompt = jsonpickle.encode(items, unpicklable=False, make_refs=False)
        user_prompt = string_utils.remove_excess_whitespace(user_prompt)
        if not user_prompt:
            user_prompt = "No items provided."
        return self._run(system_prompt, user_prompt, verify=verify)

    def _run(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        verify: bool = False,
    ) -> str:
        """Creates a placeholder for an LLM edit.

        Convenience function to run the common parts of all run commands.

        Args:
            system_prompt: The system prompt for the LLM.
            user_prompt: The user prompt for the LLM.
            verify: If True, runs with self-assessment. Defaults to False.

        Returns:
            The placeholder for the LLM edit.
        """
        logger.log(
            LOGGER_PHI_LOGGING_LEVEL,
            "Running LLM with system prompt: %s",
            system_prompt,
        )
        logger.log(
            LOGGER_PHI_LOGGING_LEVEL,
            "Running LLM with user prompt: %s",
            user_prompt,
        )

        if verify:
            replacement = self.client.chain_of_verification(
                system_prompt,
                user_prompt,
                create_new_questions=True,
            )
        else:
            replacement = self.client.run(system_prompt, user_prompt)
        placeholder_uuid = str(uuid.uuid4())
        self.placeholders.append(LlmPlaceholder(placeholder_uuid, replacement))
        return placeholder_uuid

    @property
    def child_info(self) -> str:
        """Returns the child information for the LLM."""
        return string_utils.remove_excess_whitespace(f"""
            In case the child's name or pronouns are needed for the text, they are as
            follows:
            Child name: {self.child_name}.
            Child pronouns: {string_utils.join_with_oxford_comma(self.child_pronouns)}.
        """)
