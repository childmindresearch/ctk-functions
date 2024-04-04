"""Configuration module for the ctk_functions package."""

import functools
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


@functools.lru_cache()
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()  # type: ignore
