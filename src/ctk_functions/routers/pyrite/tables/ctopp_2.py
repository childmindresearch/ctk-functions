"""Gets the CTOPP-2 data."""

import dataclasses

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
    Ctopp2RowLabels(name="Rapid Digit Naming", score_column="CTOPP_RD_S"),
    Ctopp2RowLabels(name="Rapid Letter Naming", score_column="CTOPP_RL_S"),
    Ctopp2RowLabels(name="Rapid Object Naming", score_column="CTOPP_RO_S"),
    Ctopp2RowLabels(name="Rapid Color Naming", score_column="CTOPP_NR_S"),
)


class Ctopp2DataSource(base.DataProducer):
    """Fetches the data for the CTOPP-2 table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the CTOPP-2 data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.Ctopp2)
        header = [
            base.WordTableCell(content="CTOPP - 2 Rapid Naming"),
            base.WordTableCell(content="Number of Errors"),
        ]
        content_rows = [
            [
                base.WordTableCell(content=label.name),
                base.WordTableCell(content=getattr(data, label.score_column) or "N/A"),
            ]
            for label in CTOPP2_ROW_LABELS
        ]

        return base.WordTableMarkup(rows=[header, *content_rows])
