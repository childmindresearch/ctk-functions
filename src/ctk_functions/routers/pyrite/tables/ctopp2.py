"""Gets the CTOPP-2 data."""

import dataclasses
import functools

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class Ctopp2RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        score_column: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    score_column: str


# Defines the rows and their order of appearance.
CTOPP2_ROW_LABELS = (
    Ctopp2RowLabels(name="Rapid Digit Naming", score_column="RD_errors"),
    Ctopp2RowLabels(name="Rapid Letter Naming", score_column="RL_errors"),
    Ctopp2RowLabels(name="Rapid Object Naming", score_column="RO_errors"),
    Ctopp2RowLabels(name="Rapid Color Naming", score_column="RC_errors"),
)


class _Ctopp2DataSource(base.DataProducer):
    """Fetches the data for the CTOPP-2 table."""

    test_ids = ("ctopp_2",)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the CTOPP-2 data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The text contents of the Word table.
        """
        data = utils.fetch_participant_row("person_id", mrn, models.Ctopp2)
        header = ("CTOPP - 2 Rapid Naming", "Number of Errors")
        content = [
            (label.name, getattr(data, label.score_column))
            for label in CTOPP2_ROW_LABELS
            if getattr(data, label.score_column) is not None
        ]
        return header, *content


class Ctopp2Table(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the CTOPP2 table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the CTOPP2 renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _Ctopp2DataSource
        self.formatters = base.FormatProducer.produce(
            n_rows=len(self.data_source.fetch(mrn)), column_widths=(None, None)
        )
