"""Controller for the LLM model."""

import asyncio

import pydantic

from ctk_functions.core import config, word
from ctk_functions.microservices import cloai_service
from ctk_functions.routers.hbn_report_summary import prompt

settings = config.get_settings()


async def report_summary(
    user_prompt: str,
) -> str:
    """Generates a summary for a clinical report.

    Args:
        user_prompt: The clinical report.
    """
    client = cloai_service.Client()
    diagnoses_promise = _extract_diagnoses(client, user_prompt)
    participant_promise = _extract_participant(client, user_prompt)

    diagnoses, participant = await asyncio.gather(
        diagnoses_promise, participant_promise
    )


class Diagnosis(pydantic.BaseModel):
    """Dataclass for an extracted diagnosis."""

    code: str
    name: str


class Diagnoses(pydantic.BaseModel):
    """Dataclass for the extracted diagnoses."""

    diagnoses: list[Diagnosis]


class Participant(pydantic.BaseModel):
    """Dataclass for the extracted participant."""

    first_name: str

    @property
    def possessive(self) -> str:
        return self.first_name + "'" + ("s" if self.first_name[-1] != "s" else "")


async def _extract_diagnoses(
    client: cloai_service.Client, user_prompt: str
) -> Diagnoses:
    """Extracts diagnoses from the clinical report."""
    return await client.call_instructor(
        Diagnoses, prompt.Prompts.EXTRACT_DIAGNOSIS, user_prompt
    )


async def _extract_participant(client: cloai_service.Client, user_prompt: str) -> str:
    """Extracts patient name from the clinical report."""
    return await client.call_instructor(
        Participant, prompt.Prompts.EXTRACT_PARTICIPANT, user_prompt
    )


class ReportStructure(pydantic.BaseModel):
    participant: Participant
    diagnoses: Diagnoses

    def _write_introduction(self) -> word.ParagraphSection:
        return word.ParagraphSection(
            content=(
                "We appreciate your time and patience during "
                f"{self.participant.possessive}"
                "participation at the Healthy Brain Network. This letter is a summary "
                "of the results of the assessments. The results are based on the "
                "information you provided, the information "
                f"{self.participant.first_name} provided, and the results of the "
                "assessments. For more detailed information, please refer to the "
                " clinical report."
            )
        )

    def _write_diagnoses(self) -> tuple[word.ParagraphSection, ...]:
        if len(self.diagnoses.diagnoses) == 0:
            return (
                word.ParagraphSection(
                    content=(
                        "Your child's assessment results did not lead to any diagnoses."
                    )
                ),
            )

        return (
            word.ParagraphSection(
                content=(
                    "Your child's assessment results led to the following diagnoses:"
                )
            ),
            word.ParagraphSection(content=""),
            *[
                word.ParagraphSection(content=diagnosis.name, style="List Bullet")
                for diagnosis in self.diagnoses.diagnoses
            ],
        )

    def _write_closing_paragraph(
        self,
    ) -> tuple[word.ParagraphSection, word.ParagraphSection]:
        return (
            word.ParagraphSection(
                content=(
                    "The evaluation provides helpful insight into "
                    f"{self.participant.possessive} strengths and areas in which "
                    "support may be needed. Accordingly, it will be beneficial for "
                    "{self.participant.first_name} and you to work with qualified "
                    "professionals to address areas of concern."
                )
            ),
            word.ParagraphSection(
                content=(
                    "On behalf of the Health Brain Network at the Child Mind "
                    f"Institute, thank you and {self.participant.first_name} for your "
                    "patience and commitment to completing this evaluation. We hope "
                    "that the results will be helpful."
                )
            ),
        )
