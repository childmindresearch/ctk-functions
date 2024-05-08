"""Module for syntax and grammatical correctionss of text."""

from typing import Any

import language_tool_python

LANGUAGE_TOOL = language_tool_python.LanguageTool("en-US")


class TextCorrections:
    """Makes grammatical corrections to an input text."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Placeholder to maintain compatibility with the original implementation.

        TODO: Before merging remove.
        """
        pass

    @classmethod
    def correct(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        return LANGUAGE_TOOL.correct(text)
