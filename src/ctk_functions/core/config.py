"""Configuration module for the ctk_functions package."""

import functools
import logging
import pathlib
from typing import Self

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """App settings."""

    DATA_DIR: pydantic.DirectoryPath = pathlib.Path(__file__).parent.parent / "data"
    REDCAP_API_TOKEN: pydantic.SecretStr
    REDCAP_ENDPOINT: pydantic.HttpUrl = pydantic.HttpUrl(
        "https://redcap.healthybrainnetwork.org/redcap/api/",
    )

    AWS_ACCESS_KEY_ID: pydantic.SecretStr
    AWS_SECRET_ACCESS_KEY: pydantic.SecretStr
    AWS_REGION: str = "us-west-2"

    AZURE_OPENAI_API_KEY: pydantic.SecretStr
    AZURE_OPENAI_LLM_DEPLOYMENT: pydantic.SecretStr
    AZURE_OPENAI_ENDPOINT: pydantic.SecretStr

    LOGGER_VERBOSITY: int = logging.INFO
    LOGGER_PHI_LOGGING_LEVEL: int = pydantic.Field(1, lt=logging.DEBUG)
    LOG_PHI: bool = pydantic.Field(
        default=False,
        description=(
            "Safe-guard against accidentally setting the logger verbosity "
            "below the PHI logging level."
        ),
    )

    @pydantic.model_validator(mode="after")
    def check_phi_logging(self) -> Self:
        """Checks if the PHI logging level is set too low."""
        if self.LOGGER_PHI_LOGGING_LEVEL >= self.LOGGER_VERBOSITY and not self.LOG_PHI:
            msg = (
                "The logging level may only be lower than the PHI logging level "
                "if LOG_PHI is set to True."
            )

            raise ValueError(msg)

        if self.LOG_PHI and self.LOGGER_VERBOSITY > self.LOGGER_PHI_LOGGING_LEVEL:
            msg = (
                "The PHI logging level may not be lower than the logger verbosity "
                "when LOG_PHI is set to True."
            )

            raise ValueError(msg)
        return self


@functools.lru_cache
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()


def get_logger() -> logging.Logger:
    """Gets the ctk-functions logger."""
    logger = logging.getLogger("ctk-functions")
    if logger.hasHandlers():
        return logger

    logger.setLevel(get_settings().LOGGER_VERBOSITY)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
