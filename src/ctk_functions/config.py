"""Configuration module for the ctk_functions package."""

import functools
import logging
import pathlib

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """App settings."""

    DATA_DIR: pydantic.DirectoryPath = pathlib.Path(__file__).parent / "data"
    REDCAP_API_TOKEN: pydantic.SecretStr
    REDCAP_ENDPOINT: pydantic.HttpUrl = pydantic.HttpUrl(
        "https://redcap.healthybrainnetwork.org/redcap/api/"
    )
    AZURE_BLOB_CONNECTION_STRING: pydantic.SecretStr
    LANGUAGE_TOOL_ENDPOINT: pydantic.HttpUrl = pydantic.Field(
        ..., json_schema_extra={"env": "LANGUAGE_TOOL_ENDPOINT"}
    )

    LOGGER_VERBOSITY: int = 20


@functools.lru_cache()
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()  # type: ignore


def get_logger() -> logging.Logger:
    """Gets the ctk-functions logger."""
    logger = logging.getLogger("ctk-functions")
    logger.setLevel(get_settings().LOGGER_VERBOSITY)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
