"""Gets the data for the CELF-5 Table."""

import functools

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import sql_data, types
from ctk_functions.routers.pyrite.tables import base


class _Celf5DataSource(base.DataProducer):
    """Fetches the data for the Celf5 table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[types.TestId, ...]:  # noqa: ARG003
        return ("celf_5",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the Celf5 data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = sql_data.fetch_participant_row("EID", mrn, models.Celf5)
        cutoff = (
            "Meets criterion cutoff"
            if data.CELF_ExceedCutoff
            else "Does not meet criterion cutoff"
        )
        return (
            ("Test", "Total Score", "Age Based Cutoff", "Range"),
            (
                "CELF-5 Screener",
                f"{data.CELF_Total:.0f}",
                f"{data.CELF_CriterionScore:.0f}",
                cutoff,
            ),
        )


class Celf5Table(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the CELF5 table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the CELF5 renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _Celf5DataSource
        self.formatters = base.FormatProducer.produce(
            n_rows=2, column_widths=[None] * 4
        )
