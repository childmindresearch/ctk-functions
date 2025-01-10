"""Business logic for the intake endpoints."""

import io

import fastapi
import pydantic
from fastapi import status

from ctk_functions.core import config, exceptions
from ctk_functions.microservices import redcap
from ctk_functions.routers.intake.intake_processing import parser, writer

logger = config.get_logger()


async def get_intake_report(
    survey_id: str,
    enabled_tasks: writer.EnabledTasks | None = None,
) -> bytes:
    """Generates an intake report for a survey.

    Args:
        survey_id: The survey ID.
        enabled_tasks: Developer testing setting to reduce the amount of processing.

    Returns:
        The .docx file bytes.
    """
    logger.debug("Entered controller of get_intake_report.")
    try:
        intake_data = redcap.get_intake_data(survey_id)
    except (pydantic.ValidationError, exceptions.RedcapError) as error:
        raise fastapi.HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Could not process the intake data for this MRN, please contact the "
                "development team."
            ),
        ) from error
    parsed_data = parser.IntakeInformation(intake_data)
    report = writer.ReportWriter(parsed_data, enabled_tasks)
    await report.transform()

    logger.debug("Successfully generated intake report.")
    out = io.BytesIO()
    report.report.document.save(out)
    return out.getvalue()
