"""Client to connect to the SQL server."""

import contextlib
from collections.abc import Generator

import sqlalchemy
from sqlalchemy.orm import session

from ctk_functions.core import config

settings = config.get_settings()

engine = sqlalchemy.create_engine(
    "postgresql://"
    + settings.POSTGRES_USER
    + ":"
    + settings.POSTGRES_PASSWORD.get_secret_value()
    + "@"
    + settings.POSTGRES_HOST
    + ":"
    + str(settings.POSTGRES_PORT)
    + "/"
    + settings.POSTGRES_DATABASE
)


@contextlib.contextmanager
def get_session() -> Generator[session.Session, None, None]:
    """Gets an active session and auto-closes it."""
    sess = session.Session(engine)
    try:
        yield sess
    finally:
        sess.close()
