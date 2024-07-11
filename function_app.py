"""Entrypoint for the Azure Functions app."""

import http
import json
import typing

from azure import functions

from ctk_functions import config, exceptions
from ctk_functions.functions.file_conversion import (
    controller as file_conversion_controller,
)
from ctk_functions.functions.intake import controller as intake_controller
from ctk_functions.functions.llm import controller as llm_controller
from ctk_functions.microservices import llm

logger = config.get_logger()

app = functions.FunctionApp()


@app.function_name(name="llm")
@app.route(route="llm", auth_level=functions.AuthLevel.FUNCTION, methods=["POST"])
async def llm_endpoint(req: functions.HttpRequest) -> functions.HttpResponse:
    """Runs a large language model.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the output text.
    """
    body_dict = json.loads(req.get_body().decode("utf-8"))
    system_prompt = body_dict.get("system_prompt")
    user_prompt = body_dict.get("user_prompt")
    model = body_dict.get("model")
    if not system_prompt or not user_prompt or not model:
        return functions.HttpResponse(
            "Please provide a system prompt, a user prompt, and a model name.",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
    if model not in typing.get_args(llm.VALID_LLM_MODELS):
        return functions.HttpResponse(
            "Invalid model, valid models are: "
            + ", ".join(typing.get_args(llm.VALID_LLM_MODELS))
            + ".",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )

    logger.info("Running LLM with model: %s", model)
    text = await llm_controller.run_llm(model, system_prompt, user_prompt)
    return functions.HttpResponse(
        body=text,
        status_code=http.HTTPStatus.OK,
    )


@app.function_name(name="IntakeReport")
@app.route(
    route="intake-report/{survey_id}",
    auth_level=functions.AuthLevel.FUNCTION,
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
    model = req.headers.get("X-Model")
    if not survey_id or not model:
        return functions.HttpResponse(
            "Please provide a survey ID and model name.",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
    if model not in typing.get_args(llm.VALID_LLM_MODELS):
        return functions.HttpResponse(
            "Invalid model, valid models are: "
            + ", ".join(typing.get_args(llm.VALID_LLM_MODELS))
            + ".",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )

    logger.info(
        "Generating intake report for identifier %s with model %s.", survey_id, model
    )
    try:
        docx_bytes = await intake_controller.get_intake_report(survey_id, model)
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
    route="markdown2docx", auth_level=functions.AuthLevel.FUNCTION, methods=["POST"]
)
async def markdown2docx(req: functions.HttpRequest) -> functions.HttpResponse:
    """Converts a Markdown document to a .docx file.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the .docx file.
    """
    body_dict = json.loads(req.get_body().decode("utf-8"))
    correct_they = req.headers.get("X-Correct-They", False)
    correct_capitalization = req.headers.get("X-Correct-Capitalization", False)
    markdown = body_dict.get("markdown", None)
    if not markdown:
        return functions.HttpResponse(
            "Please provide a Markdown document.",
            status_code=http.HTTPStatus.BAD_REQUEST,
        )
    logger.info("Converting Markdown to .docx")
    docx_bytes = file_conversion_controller.markdown2docx(
        markdown,
        correct_they=correct_they,
        correct_capitalization=correct_capitalization,
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
