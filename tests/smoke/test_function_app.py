"""Smoke tests for the function app module."""

import inspect
import json

import function_app
from azure.functions.decorators import function_app as azure_function_app


def get_function_auth_level(
    function: azure_function_app.FunctionBuilder,
) -> str:
    """Gets the auth level of a function."""
    settings = json.loads(function._function.get_function_json())
    return settings["bindings"][0]["authLevel"]


def test_function_auth_level() -> None:
    """Tests that no function has the anonymous auth level."""
    endpoints = inspect.getmembers(
        function_app,
        lambda attribute: isinstance(attribute, azure_function_app.FunctionBuilder),
    )
    allowed_auth_levels = ["FUNCTION", "ADMIN"]

    for name, endpoint in endpoints:
        auth_level = get_function_auth_level(endpoint)

        assert auth_level in allowed_auth_levels, f"{name} has the wrong auth level."
