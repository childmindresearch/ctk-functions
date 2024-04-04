"""Entrypoint for the Azure Functions app."""

import tempfile

from azure import functions

from ctk_functions.intake import parser, writer
from ctk_functions.microservices import redcap

app = functions.FunctionApp()


@app.function_name(name="get-intake-report")
@app.route(route="intake-report/{survey_id}", auth_level=functions.AuthLevel.FUNCTION)
async def main(req: functions.HttpRequest) -> functions.HttpResponse:
    """Generates an intake report for a survey.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the .docx file.
    """
    survey_id = req.route_params.get("survey_id")
    if survey_id is None:
        return functions.HttpResponse("Please provide a survey ID.", status_code=400)

    intake_data = redcap.get_intake_data(survey_id)
    parsed_data = parser.IntakeInformation(intake_data.to_dict())
    report = writer.ReportWriter(parsed_data)
    await report.transform()

    with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
        report.report.save(temp_file.name)
        with open(temp_file.name, "rb") as file:
            file_contents = file.read()
            return functions.HttpResponse(
                body=file_contents,
                status_code=200,
            )
