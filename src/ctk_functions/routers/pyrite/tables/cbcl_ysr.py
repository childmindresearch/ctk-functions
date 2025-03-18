"""Module for inserting the CBCL and YSR tables."""

import dataclasses
from typing import Any, Literal

import cmi_docx
import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils

# There are two sets of thresholds for clinical relevance.
# The one with higher scores is denoted as "HIGH", the other as "LOW".
CLINICAL_RELEVANCE_HIGH = (
    utils.ClinicalRelevance(
        low=None,
        high=65,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=65,
        high=70,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=70,
        high=None,
        label="clinically relevant",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)

CLINICAL_RELEVANCE_LOW = (
    utils.ClinicalRelevance(
        low=None,
        high=60,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    utils.ClinicalRelevance(
        low=60,
        high=65,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    utils.ClinicalRelevance(
        low=65,
        high=None,
        label="clinically relevant",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
)


@dataclasses.dataclass
class RowLabels:
    """Defines the rows of the table.

    Attributes:
        name: Name of the score, used in the first column.
        acronym: Acronym of the row, used for accessing the SQL data.
    """

    name: str
    acronym: str
    relevance: tuple[
        utils.ClinicalRelevance,
        utils.ClinicalRelevance,
        utils.ClinicalRelevance,
    ]


# Defines the rows and their order of appearance.
ROW_LABELS = (
    RowLabels(
        name="Anxious/Depressed",
        acronym="AD",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(
        name="Withdrawn/Depressed",
        acronym="WD",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(
        name="Somatic Complaints",
        acronym="SC",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(name="Social Problems", acronym="SP", relevance=CLINICAL_RELEVANCE_HIGH),
    RowLabels(name="Thought Problems", acronym="TP", relevance=CLINICAL_RELEVANCE_HIGH),
    RowLabels(
        name="Attention Problems",
        acronym="AP",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(
        name="Rule Breaking Behaviors",
        acronym="RBB",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(
        name="Aggressive Behaviors",
        acronym="AB",
        relevance=CLINICAL_RELEVANCE_HIGH,
    ),
    RowLabels(
        name="Internalizing (Emotional) Problems",
        acronym="Int",
        relevance=CLINICAL_RELEVANCE_LOW,
    ),
    RowLabels(
        name="Externalizing (Behavioral) Problems",
        acronym="Ext",
        relevance=CLINICAL_RELEVANCE_LOW,
    ),
    RowLabels(name="Total Problems", acronym="Total", relevance=CLINICAL_RELEVANCE_LOW),
)


class Cbcl(base.BaseTable):
    """Fetches and creates the Child Behavior Checklist table."""

    def _get_data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Fetches the data for the CBCL table.

        Returns:
            The participant's CBCL table row.
        """
        statement = sqlalchemy.select(
            models.t_I2B2_Export_CBCL_t,
        ).where(
            self.eid == models.t_I2B2_Export_CBCL_t.c.EID,  # type: ignore[arg-type]
        )

        with client.get_session() as session:
            return session.execute(statement).fetchone()

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the CBCL table to the document.

        Args:
            doc: The document to add the table to.
        """
        _add_cbcl_ysr_table(doc, self._data_no_none, "cbcl")


class Ysr(base.BaseTable):
    """Fetches and creates the Youth Self Report table."""

    def _get_data(self) -> sqlalchemy.Row[tuple[Any, ...]] | None:
        """Fetches the data for the YSR table.

        Returns:
            The participants YSR table row.
        """
        statement = sqlalchemy.select(
            models.t_I2B2_Export_YSR_t,
        ).where(
            self.eid == models.t_I2B2_Export_YSR_t.c.EID,  # type: ignore[arg-type]
        )

        with client.get_session() as session:
            return session.execute(statement).fetchone()

    def add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the YSR table to the document.

        Args:
            doc: The document to add the table to.
        """
        _add_cbcl_ysr_table(doc, self._data_no_none, "ysr")


def _add_cbcl_ysr_table(
    doc: document.Document,
    data: sqlalchemy.Row[tuple[Any, ...]],
    name: Literal["cbcl", "ysr"],
) -> None:
    """Adds the CBCL or YSR table to the report.

    Args:
        doc: The word document.
        data: The subject's row from the SQL table.
        name: The name of the table.
    """
    header_texts = [
        "Subscales",
        "T-Score",
        "Clinical Relevance",
    ]

    table = doc.add_table(len(ROW_LABELS) + 1, len(header_texts))
    table.style = utils.TABLE_STYLE
    utils.add_header(table, header_texts)

    for row_index, label in enumerate(ROW_LABELS):
        row_index += 1  # noqa: PLW2901 # Offset for header row.
        table.rows[row_index].cells[0].text = label.name
        score = getattr(
            data,
            f"{name.upper()}_{label.acronym}_T",
        )
        table.rows[row_index].cells[1].text = str(score)
        for relevance in label.relevance:
            if relevance.in_range(score):
                extended_cell = cmi_docx.ExtendCell(table.rows[row_index].cells[1])
                extended_cell.format(relevance.style)
                break
        utils.set_index_column_name_or_merge(
            table,
            "\n".join([str(relevance) for relevance in label.relevance]),
            row_index,
            col_index=2,
        )
