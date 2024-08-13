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
        "https://redcap.healthybrainnetwork.org/redcap/api/",
    )

    AWS_ACCESS_KEY_ID: pydantic.SecretStr
    AWS_SECRET_ACCESS_KEY: pydantic.SecretStr

    AZURE_BLOB_CONNECTION_STRING: pydantic.SecretStr
    AZURE_OPENAI_API_KEY: pydantic.SecretStr
    AZURE_OPENAI_LLM_DEPLOYMENT: pydantic.SecretStr
    AZURE_OPENAI_ENDPOINT: pydantic.SecretStr

    LOGGER_VERBOSITY: int = logging.INFO


@functools.lru_cache
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()  # type: ignore[call-arg]


def get_logger() -> logging.Logger:
    """Gets the ctk-functions logger."""
    if logging.getLogger("ctk-functions").hasHandlers():
        return logging.getLogger("ctk-functions")
    logger = logging.getLogger("ctk-functions")
    logger.setLevel(get_settings().LOGGER_VERBOSITY)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
