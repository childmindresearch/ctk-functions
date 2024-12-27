"""Test logging in config.py."""

import contextlib
import logging
import os
from collections.abc import Generator
from typing import Any

import pytest

from ctk_functions.core import config


@contextlib.contextmanager
def set_env(**environ: str) -> Generator[None, Any, None]:
    """Temporarily set the process environment variables.

    Args:
        environ: The environment variables to set.
    """
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_get_logger(caplog: pytest.LogCaptureFixture) -> None:
    """Test the wristpy logger with level set to 20 (info)."""
    logger = config.get_logger()
    logger.propagate = True

    logger.debug("Debug message here.")
    logger.info("Info message here.")
    logger.warning("Warning message here.")

    assert logger.getEffectiveLevel() == logging.INFO
    assert "Debug message here" not in caplog.text
    assert "Info message here." in caplog.text
    assert "Warning message here." in caplog.text


def test_settings_validate_log_level_success() -> None:
    """Test the settings validate log level function with a valid log level."""
    with set_env(LOGGER_VERBOSITY="1", LOGGER_PHI_LOGGING_LEVEL="2", LOG_PHI="True"):
        settings = config.Settings()

    assert settings.LOGGER_VERBOSITY == 1
    assert settings.LOGGER_PHI_LOGGING_LEVEL == 2  # noqa: PLR2004
    assert settings.LOG_PHI


def test_settings_validate_log_level_verbosity_too_low() -> None:
    """Test the settings validate log level function with an invalid log level."""
    with (
        set_env(LOGGER_VERBOSITY="1", LOGGER_PHI_LOGGING_LEVEL="2", LOG_PHI="False"),
        pytest.raises(ValueError, match="The logging level may only be lower.*"),
    ):
        config.Settings()


def test_settings_validate_log_level_verbosity_too_high() -> None:
    """Test the settings validate log level function with an invalid log level."""
    with (
        set_env(LOGGER_VERBOSITY="2", LOGGER_PHI_LOGGING_LEVEL="1", LOG_PHI="True"),
        pytest.raises(ValueError, match="The PHI logging level.*"),
    ):
        config.Settings()
