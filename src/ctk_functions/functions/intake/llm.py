"""Make edits to the clinical report using a large language model."""

from cloai import openai_api


class LlmEditor:
    """Editor powered by a Large Language Model."""

    def __init__(self) -> None:
        """Creates an editor powered by a Large Language Model."""
        self.llm = openai_api.ChatCompletion(api_key="INTENTIONALLY_DEFUNCT")

    async def run(self, excerpt: str, parent_input: str, placeholder: str) -> str:
        """Inserts the parent's response into the excerpt.

        Args:
            question: The question asked to the parent.
            excerpt: The clinical report excerpt with a placeholder.
            parent_input: The parent's response to the question.
            placeholder: The placeholder in the excerpt.
        """
        user_prompt = f"""
Placeholder: "{placeholder}"

Clinical report excerpt: "{excerpt}"

Parent Response: "{parent_input}"
            """

        system_prompt = """
    You will receive an excerpt of a clinical report with part of the text
    replaced by a placeholder as well as a response by a parent. Your task is to
    insert the parent's response into the excerpt. You should return the excerpt
    in full with the placeholder replaced by the parent's response. The full
    response should be no more than two sentences long.
"""

        return self.llm.run(user_prompt, system_prompt)
