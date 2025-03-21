"""Module for the WISC tables."""

import dataclasses

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class WiscCompositeRowLabels:
    """Defines the rows of the composite table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used in the first
            column and for accessing the SQL data.
    """

    name: str
    acronym: str


WISC_COMPOSITE_ROW_LABELS = (
    WiscCompositeRowLabels(name="Verbal Comprehension", acronym="VCI"),
    WiscCompositeRowLabels(name="Visual Spatial", acronym="VSI"),
    WiscCompositeRowLabels(name="Fluid Reasoning", acronym="FRI"),
    WiscCompositeRowLabels(name="Working Memory", acronym="WMI"),
    WiscCompositeRowLabels(name="Processing Speed", acronym="PSI"),
    WiscCompositeRowLabels(name="Full Scale IQ", acronym="FSIQ"),
)


class WiscComposite(base.BaseTable[models.Wisc5]):
    """Fetches data for and creates the WISC composite table."""

    _title = "The Wechsler Intelligence Scale for Children-Fifth Edition (WISC-V)"

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[models.Wisc5]]:
        return sqlalchemy.select(models.Wisc5).where(
            self.eid == models.Wisc5.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the WISC composite table to the report."""
        table = doc.add_table(len(WISC_COMPOSITE_ROW_LABELS) + 1, 4)
        table.style = utils.TABLE_STYLE
        header_texts = [
            "Composite",
            "Standard Score",
            "Percentile",
            "Range",
        ]
        utils.add_header(table, header_texts)

        for index, label in enumerate(WISC_COMPOSITE_ROW_LABELS):
            index += 1  # Offset for the header row.  # noqa: PLW2901
            row = table.template_rows[index].cells
            row[0].text = f"{label.name} ({label.acronym})"
            score = getattr(self.data_no_none, f"WISC_{label.acronym}")

            percentile = utils.standard_score_to_percentile(score)
            row[1].text = str(score)
            row[2].text = str(percentile)
            row[3].text = utils.standard_score_to_qualifier(
                score,
            )
