"""Module for the WISC tables_old."""

import dataclasses
import functools

from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import sql_data, types
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(5.49),
    shared.Cm(3.5),
    shared.Cm(3.38),
    shared.Cm(4.12),
)


@dataclasses.dataclass
class WiscCompositeRowLabels:
    """Defines the rows of the composite table.

    Attributes:
        name: Name of the score, used in the first column.
        score_column: Acronym of the row, used in the first
            column and for accessing the SQL data.
    """

    name: str
    score_column: str


WISC_COMPOSITE_ROW_LABELS = (
    WiscCompositeRowLabels(name="Verbal Comprehension (VCI)", score_column="WISC_VCI"),
    WiscCompositeRowLabels(name="Visual Spatial (VSI)", score_column="WISC_VSI"),
    WiscCompositeRowLabels(name="Fluid Reasoning (FRI)", score_column="WISC_FRI"),
    WiscCompositeRowLabels(name="Working Memory (WMI)", score_column="WISC_WMI"),
    WiscCompositeRowLabels(name="Processing Speed (PSI)", score_column="WISC_PSI"),
    WiscCompositeRowLabels(name="Full Scale IQ (FSIQ)", score_column="WISC_FSIQ"),
)


class _WiscCompositeDataSource(base.DataProducer):
    """Fetches data for and creates the WISC composite table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[types.TestId, ...]:  # noqa: ARG003
        return ("wisc_5",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = sql_data.fetch_participant_row("EID", mrn, models.Wisc5)
        header = ("Composite", "Standard Score", "Percentile", "Range")
        content_rows = [
            cls._create_wisc_composite_row(data, label)
            for label in WISC_COMPOSITE_ROW_LABELS
        ]
        return header, *content_rows

    @staticmethod
    def _create_wisc_composite_row(
        data: models.Wisc5,
        label: WiscCompositeRowLabels,
    ) -> tuple[str, str, str, str]:
        score = getattr(data, label.score_column)
        percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
        qualifier = utils.standard_score_to_qualifier(score)

        return label.name, score, f"{percentile:.0f}", qualifier


class WiscCompositeTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the WISC composite table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the WISC renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _WiscCompositeDataSource
        self.formatters = base.FormatProducer.produce(
            n_rows=len(WISC_COMPOSITE_ROW_LABELS) + 1,
            column_widths=COLUMN_WIDTHS,
        )
