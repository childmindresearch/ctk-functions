"""Business logic for the intake endpoints."""

import tempfile

from ctk_functions.functions.intake import parser, writer
from ctk_functions.microservices import llm, redcap


async def get_intake_report(survey_id: str, model: llm.VALID_LLM_MODELS) -> bytes:
    """Generates an intake report for a survey.

    Args:
        survey_id: The survey ID.
        model: The model to use for the language model.

    Returns:
        The .docx file bytes.
    """
    intake_data = redcap.get_intake_data(survey_id)
    parsed_data = parser.IntakeInformation(intake_data)
    report = writer.ReportWriter(parsed_data)
    await report.transform()

    with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
        report.report.save(temp_file.name)
        temp_file.seek(0)
        return temp_file.read()
