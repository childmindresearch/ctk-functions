"""Entrypoint for the Azure Functions app."""

import http
import json

from azure import functions

from ctk_functions import config, exceptions
from ctk_functions.functions.file_conversion import (
    controller as file_conversion_controller,
)
from ctk_functions.functions.intake import controller as intake_controller

logger = config.get_logger()

app = functions.FunctionApp()


@app.function_name(name="IntakeReport")
@app.route(
    route="intake-report/{survey_id}",
    auth_level=functions.AuthLevel.ANONYMOUS,
    methods=["GET"],
)
async def get_intake_report(req: functions.HttpRequest) -> functions.HttpResponse:
    """Generates an intake report for a survey.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the .docx file.
    """
    survey_id = req.route_params.get("survey_id")
    if not survey_id:
        return functions.HttpResponse(
            "Please provide a survey ID.", status_code=http.HTTPStatus.BAD_REQUEST
        )

    try:
        docx_bytes = await intake_controller.get_intake_report(survey_id)
    except exceptions.RedcapException as exc_info:
        logger.error(exc_info)
        return functions.HttpResponse(
            str(exc_info), status_code=http.HTTPStatus.BAD_REQUEST
        )

    return functions.HttpResponse(
        body=docx_bytes,
        status_code=http.HTTPStatus.OK,
    )


@app.function_name(name="MarkdownToDocx")
@app.route(
    route="markdown2docx", auth_level=functions.AuthLevel.ANONYMOUS, methods=["POST"]
)
async def markdown2docx(req: functions.HttpRequest) -> functions.HttpResponse:
    """Converts a Markdown document to a .docx file.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the .docx file.
    """
    body_dict = json.loads(req.get_body().decode("utf-8"))
    correct_they = body_dict.get("correct_they", False)
    markdown = body_dict.get("markdown", None)
    if not markdown:
        return functions.HttpResponse(
            "Please provide a Markdown document.",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
    docx_bytes = file_conversion_controller.markdown2docx(
        markdown, correct_they=correct_they
    )
    return functions.HttpResponse(
        body=docx_bytes,
        status_code=http.HTTPStatus.OK,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.function_name(name="Health")
@app.route(route="health", auth_level=functions.AuthLevel.FUNCTION, methods=["GET"])
async def health(req: functions.HttpRequest) -> functions.HttpResponse:
    """Health check endpoint.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response indicating the health of the app.
    """
    return functions.HttpResponse(
        body="Healthy",
        status_code=http.HTTPStatus.OK,
    )
