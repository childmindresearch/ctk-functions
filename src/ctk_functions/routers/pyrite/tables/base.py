"""Base class definition for all tables."""

import abc
from typing import Any

import pydantic
import sqlalchemy
from docx import document


class TableDataNotFoundError(Exception):
    """Error raised when table data cannot be found."""


class BaseTable(pydantic.BaseModel, abc.ABC):
    """Abstract base class for all Pyrite tables."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    eid: str = pydantic.Field(..., frozen=True)

    @pydantic.computed_field
    def data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Cached data property that is only computed on request."""
        return self._get_data()

    @property
    def _data_no_none(self) -> sqlalchemy.Row[tuple[Any, ...]]:
        """Copy of the data that raises an error on None.

        Used to coalesce all None checks in one place.
        """
        if self.data is None:
            msg = "Data is None, cannot add this table."
            raise TableDataNotFoundError(msg)
        return self.data  # type: ignore[return-value] # Mypy incorrectly identifies data as Callable.

    @abc.abstractmethod
    def _get_data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Abstract data fetcher.

        Returns:
            The data required to construct the table.
        """

    @abc.abstractmethod
    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the table to the document.

        Args:
            doc: The Word document.
        """
