"""Base class definition for all tables_old."""

import abc
from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

import cmi_docx
import pydantic
import sqlalchemy
from docx import document, table

from ctk_functions.core import config
from ctk_functions.microservices.sql import client

T = TypeVar("T")

logger = config.get_logger()


class TableDataNotFoundError(Exception):
    """Thrown when a table's data is not found."""


class ConditionalStyle(pydantic.BaseModel):
    """Applies a style conditional upon a cell's contents.

    Args:
        condition: The condition, if it evaluates to True then the style
            will be applied.
        style: The style to apply.
    """

    condition: Callable[[str], bool]
    style: cmi_docx.TableStyle

    def apply(self, cells: table._Cell | Iterable[table._Cell]) -> None:
        """Applies the style to the cell if the condition is met.

        Args:
            cells: The cells to apply the style to.

        """
        if isinstance(cells, table._Cell):  # noqa: SLF001
            cells = (cells,)

        for cell in cells:
            if self.condition(cell.text):
                cmi_docx.ExtendCell(cell).format(self.style)


class ClinicalRelevance(pydantic.BaseModel):
    """Stores the score ranges for clinical relevance.

    Attributes:
        low: Minimum (exclusive) score for this tier of relevance.
        high: Maximum (inclusive) score for this tier of relevance.
        label: Label for this tier of relevance.
        style: Custom cell styling for this tier of relevance.
    """

    low: int | None
    high: int | None
    label: str | None
    style: cmi_docx.TableStyle

    def in_range(self, value: float | str) -> bool:
        """Checks if value is within the valid range.

        Excludes low value, includes high value.
        """
        value = float(value)
        if not self.high:
            return value > self.low  # type: ignore[operator]
        if not self.low:
            return value <= self.high
        return self.low < value <= self.high

    def __str__(self) -> str:
        """String representation of the clinical relevance.

        Returns:
            A string denoting the range for this tier's relevance.

        Example outputs:
            "<65 = LABEL" if low is 65, high is not set.
            ">65 = LABEL" if low is not set and high is 65.
            "65-65 = LABEL" if low is 65 and high is 75.
        """
        if self.low is None:
            value = f"<{self.high}"

        elif self.high is None:
            value = f">{self.low}"
        else:
            value = f"{self.low}-{self.high}"

        if self.label:
            return f"{value} = {self.label}"
        return value


class Formatter(pydantic.BaseModel):
    """Formatter for table cells.

    Attributes:
        conditional_styles: A tuple of styles to apply, conditional on cell contents.
        merge_top: If True, merges cells with identical cells above them.
        merge_right: If True, merges cells with identical cells right of them.

    """

    conditional_styles: list[ConditionalStyle] = pydantic.Field(
        default_factory=list,
    )
    merge_top: bool = pydantic.Field(default=False)
    merge_right: bool = pydantic.Field(default=False)

    def format(self, tbl: table.Table, row_index: int, col_index: int) -> None:
        """Formats the cell content for a table.

        Args:
            tbl: The table to format.
            row_index: The row index of the target cell.
            col_index: The column index of the target cell.
        """
        if row_index == 0 and self.merge_top:
            msg = "Cannot merge top row upwards."
            raise ValueError(msg)
        if col_index == len(tbl.rows[0].cells) and self.merge_right:
            msg = "Cannot merge right row rightwards."
            raise ValueError(msg)

        cell = tbl.rows[row_index].cells[col_index]
        for style in self.conditional_styles:
            style.apply(cell)

        if self.merge_top:
            prev_cell = tbl.rows[row_index - 1].cells[col_index]
            current_text = cell.text

            if prev_cell.text == cell.text:
                prev_cell.merge(cell)
                prev_cell.text = current_text

        if self.merge_right:
            next_cell = tbl.rows[row_index].cells[col_index + 1]
            current_text = cell.text
            if next_cell.text == cell.text:
                next_cell.merge(cell)
                cell.text = current_text


class TableCell(Generic[T], pydantic.BaseModel):
    """Definition of a cell in a table.

    Attributes:
        content: If a string, the cell contents will be that string. If
            a Callable, the Callable will be used to dynamically get the
            contents from a data dictionary.
        formatter: Styling for the cell.
    """

    content: str | Callable[[T], str]
    formatter: Formatter = Formatter()

    def render(self, row_data: T | None = None) -> str:
        """Render the content based on the data.

        Args:
            row_data: Dictionary containing the SQL query result for a row.
                If self.content is a Callable, the Callable will be called on
                this.

        Returns:
            The cell contents.
        """
        if callable(self.content):
            if row_data is None:
                msg = "Row data required for callable content"
                raise ValueError(msg)
            return str(self.content(row_data))
        return str(self.content)


class SqlDataSource(Generic[T], pydantic.BaseModel):
    """SQL data source configuration for retrieving data."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    query: sqlalchemy.Select[tuple[T, ...]]
    _data: T | None = None
    _has_fetched_data: bool = False

    def fetch_data(
        self,
    ) -> T | None:
        """Execute the SQL query and return the results.

        This assumes that there is only one row of interest.

        Returns:
            Query results.
        """
        if self._has_fetched_data:
            return self._data

        with client.get_session() as session:
            logger.debug("Fetching data with '%s'.", self.query)
            self._data = session.execute(self.query).scalar_one_or_none()
        self._has_fetched_data = True

        return self._data


class WordTable(Generic[T], pydantic.BaseModel):
    """Creates Word tables.

    Attributes:
        data_source: The SQL data source to populate the table with.
        template_rows: Templates containing the instructions to populate the table.
        title: The title of the table.
        table_style: The name of the Word table style to use.
    """

    data_source: SqlDataSource[T]
    template_rows: list[list[TableCell[T]]]
    title: str | None = None
    table_style: str = "Grid Table 7 Colorful"

    def add(self, doc: document.Document) -> None:
        """Adds the table to the document.

        Arguments:
            doc: The document to add the table to.
        """
        built_rows = self._build()
        self._insert(doc, built_rows)

    def _build(self) -> list[list[TableCell[T]]]:
        """Build the Word table."""
        data = self.data_source.fetch_data()
        if data is None:
            msg = "No data available."
            raise TableDataNotFoundError(msg)

        built_table = []
        for row in self.template_rows:
            built_row: list[TableCell[T]] = [
                TableCell(content=cell.render(data), formatter=cell.formatter)
                for cell in row
            ]
            built_table.append(built_row)
        return built_table

    def _insert(
        self,
        doc: document.Document,
        rows: list[list[TableCell[T]]],
    ) -> None:
        """Adds the Word table to the document.

        Args:
            doc: The Word document.
            rows: An array of an array of cell contents, where the outer array
                denotes rows, and the inner arrays denote columns.
        """
        if self.title:
            doc.add_heading(
                text=self.title,
                level=1,
            )

        n_rows = len(rows)
        n_cols = len(rows[0])

        tbl = doc.add_table(n_rows, n_cols)
        tbl.style = self.table_style

        for row_index, row in enumerate(tbl.rows):
            for col_index, cell in enumerate(row.cells):
                cell.text = rows[row_index][col_index].render()
                rows[row_index][col_index].formatter.format(tbl, row_index, col_index)


class BaseTable(abc.ABC):
    """Abstract base class for all Pyrite tables."""

    def __init__(self, eid: str) -> None:
        """Initialize the table with an EID.

        Args:
            eid: The unique identifier of the participant.
        """
        self.eid = eid

    @abc.abstractmethod
    def add(self, doc: document.Document) -> None:
        """Adds the table to the document.

        Args:
            doc: The document to add the table to.
        """
