"""Entrypoint for the FastAPI server."""

import fastapi

from ctk_functions.core import config
from ctk_functions.routers.file_conversion import views as file_conversion_views
from ctk_functions.routers.intake import views as intake_views
from ctk_functions.routers.language_tool import views as language_tool_views
from ctk_functions.routers.llm import views as llm_views

logger = config.get_logger()

app = fastapi.FastAPI(
    title="Clinician Toolkit API",
    summary="Clinician toolkit functionality too complex for the webapp's backend.",
    version="0.1.0",
    swagger_ui_parameters={
        "operationsSorter": "method",
        "displayRequestDuration": True,
    },
)

app.include_router(file_conversion_views.router)
app.include_router(intake_views.router)
app.include_router(language_tool_views.router)
app.include_router(llm_views.router)


@app.get("/health")
def health_endpoint() -> fastapi.Response:
    """Health check endpoint."""
    return fastapi.Response()