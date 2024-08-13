"""Smoke tests for the function app module."""

import inspect
import json
import pathlib
import sys

from azure.functions.decorators import function_app as azure_function_app

import ctk_functions

repository_root = pathlib.Path(ctk_functions.__file__).parent.parent.parent
sys.path.insert(0, str(repository_root))

import function_app  # noqa: E402


def get_function_auth_level(
    function: azure_function_app.FunctionBuilder,
) -> str:
    """Gets the auth level of a function."""
    settings = json.loads(function._function.get_function_json())
    return settings["bindings"][0]["authLevel"]  # type: ignore[no-any-return]


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
