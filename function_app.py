"""Entrypoint for Azure Functions."""

import azure.functions as func

from ctk_functions import app as fastapi_app

app = func.AsgiFunctionApp(app=fastapi_app.app, http_auth_level=func.AuthLevel.FUNCTION)
