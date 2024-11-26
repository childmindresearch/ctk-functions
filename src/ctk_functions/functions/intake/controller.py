"""Business logic for the intake endpoints."""

import http
import io

import pydantic
from azure import functions

from ctk_functions import config, exceptions
from ctk_functions.functions.intake import parser, writer
from ctk_functions.microservices import llm, redcap

logger = config.get_logger()


async def get_intake_report(
    survey_id: str,
    model: llm.VALID_LLM_MODELS,
    enabled_tasks: writer.EnabledTasks | None = None,
) -> functions.HttpResponse:
    """Generates an intake report for a survey.

    Args:
        survey_id: The survey ID.
        model: The model to use for the language model.
        enabled_tasks: Developer testing setting to reduce the amount of processing.

    Returns:
        The .docx file bytes.
    """
    logger.debug("Entererd controller of get_intake_report.")
    try:
        intake_data = redcap.get_intake_data(survey_id)
    except (pydantic.ValidationError, exceptions.RedcapError):
        return functions.HttpResponse(
            (
                "Could not process the intake data for this MRN, please contact the "
                "development team."
            ),
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    parsed_data = parser.IntakeInformation(intake_data)
    report = writer.ReportWriter(parsed_data, model, enabled_tasks)
    await report.transform()

    logger.debug("Successfully generated intake report.")
    out = io.BytesIO()
    report.report.document.save(out)
    return functions.HttpResponse(body=out.getvalue(), status_code=http.HTTPStatus.OK)
