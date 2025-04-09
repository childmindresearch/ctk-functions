"""Client to connect to the SQL server."""

import contextlib
from collections.abc import Generator

import sqlalchemy
from sqlalchemy.orm import session

from ctk_functions.core import config

settings = config.get_settings()

engine = sqlalchemy.create_engine(
    "mssql+pyodbc://"
    + settings.MSSQL_USER
    + ":"
    + settings.MSSQL_PASSWORD.get_secret_value()
    + "@"
    + settings.MSSQL_HOST
    + ":"
    + str(settings.MSSQL_PORT)
    + "/"
    + settings.MSSQL_DATABASE
    + "?driver="
    + settings.MSSQL_DRIVER
    + "&Encrypt=no&TrustServerCertificate=no",
)


@contextlib.contextmanager
def get_session() -> Generator[session.Session, None, None]:
    """Gets an active session and auto-closes it."""
    sess = session.Session(engine)
    try:
        yield sess
    finally:
        sess.close()
