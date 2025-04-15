"""Module for inserting the language table."""

import dataclasses
import functools
from typing import Literal

import cmi_docx
import sqlalchemy
from docx import shared
from docx.enum import text

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(2.02),
    shared.Cm(6.23),
    shared.Cm(2.01),
    shared.Cm(2.2),
    shared.Cm(4.04),
)

TABLE_NAMES = Literal["SummaryScores", "Ctopp2"]


@dataclasses.dataclass
class LanguageRowLabel:
    """Definitions of the rows of the language table."""

    test: str
    subtest: str
    score_column: str | None
    table: TABLE_NAMES


LANGUAGE_ROW_LABELS = (
    LanguageRowLabel(
        test="WIAT-4",
        subtest="Listening Comprehension",
        score_column="WIAT_4_LC_Std",
        table="SummaryScores",
    ),
    LanguageRowLabel(
        test="WIAT-4",
        subtest="\tReceptive Vocabulary",
        score_column="WIAT_4_LC_RV_Std",
        table="SummaryScores",
    ),
    LanguageRowLabel(
        test="WIAT-4",
        subtest="\tOral Discourse Comprehension",
        score_column="WIAT_4_LC_ODC_Std",
        table="SummaryScores",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="Phonological Memory",
        score_column=None,
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tNon-word Repetition",
        score_column="NR_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="Phonological Awareness",
        score_column="CTOPP_PA_Comp",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tElision",
        score_column="EL_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tBlending Words",
        score_column="BW_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="Rapid Symbolic Naming",
        score_column="RSN_composite",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tRapid Digit Naming",
        score_column="RD_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tRapid Letter Naming",
        score_column="RL_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="Rapid Non-Symbolic",
        score_column="RnSN",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tRapid Object Naming",
        score_column="RO_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabel(
        test="CTOPP-2",
        subtest="\tRapid Color Naming",
        score_column="RC_standard",
        table="Ctopp2",
    ),
)


class _LanguageDataSource(base.DataProducer):
    """Fetches the data for the Language table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the Language data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = _get_data(mrn)

        header_formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        header_content = ["Test", "Subtest", "Standard Score", "Percentile", "Range"]
        header = [
            base.WordTableCell(content=content, formatter=formatter)
            for content, formatter in zip(
                header_content, header_formatters, strict=True
            )
        ]

        body_formatters = cls._get_body_formatters()
        content_rows = [
            cls._get_content_row(data, label, formatters)
            for label, formatters in zip(
                LANGUAGE_ROW_LABELS, body_formatters, strict=False
            )
        ]
        content_rows = [row for row in content_rows if row]
        return base.WordTableMarkup(rows=[header, *content_rows])

    @staticmethod
    def _get_content_row(
        data: sqlalchemy.Row[tuple[models.SummaryScores, models.Ctopp2]],
        label: LanguageRowLabel,
        formatters: list[base.Formatter],
    ) -> tuple[base.WordTableCell, ...] | None:
        """Gets the rows of the table's body.

        Note that rows without data are omitted, unless they are explicitly
        set to None in the labels, in which case they are included without
        content in the score/percentile/qualifier cells.

        Args:
            data: The participant's data for the SummaryScores and Ctopp2 tables.
            label: The definition of the requested row.
            formatters: The list of formatters to apply to the row, must be of length 5.

        Returns:
            In this order: the test cell, the subtest cell, the score cell, the
            percentile cell, and the qualifier cell.
        """
        table_indices: dict[TABLE_NAMES, int] = {
            "SummaryScores": 0,
            "Ctopp2": 1,
        }
        data_table = data[table_indices[label.table]]
        if label.score_column and not getattr(data_table, label.score_column):
            # Rows without data should be omitted.
            return None

        test_cell = base.WordTableCell(
            content=label.test,
            formatter=formatters[0],
        )
        subtest_cell = base.WordTableCell(
            content=label.subtest, formatter=formatters[1]
        )

        if not label.score_column:
            # Special handling for score_column=None
            # Add an empty row; these are label rows.
            score_cell = base.WordTableCell(content="")
            percentile_cell = base.WordTableCell(content="")
            range_cell = base.WordTableCell(content="")
        else:
            score = float(getattr(data_table, label.score_column))
            percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
            qualifier = utils.standard_score_to_qualifier(score)
            score_cell = base.WordTableCell(
                content=str(int(score)), formatter=formatters[2]
            )
            percentile_cell = base.WordTableCell(
                content=f"{percentile:.0f}", formatter=formatters[3]
            )
            range_cell = base.WordTableCell(content=qualifier, formatter=formatters[4])
        return test_cell, subtest_cell, score_cell, percentile_cell, range_cell

    @staticmethod
    def _get_body_formatters() -> list[list[base.Formatter]]:
        r"""Creates the formatters for the language table.

        The language table has a lot of specific formatting idiosyncrasies.
        Specifically: the first column should be merged, the second column
        left aligned. If the subtest (second column) is a aggregate test
        (i.e. does not start with a \t), then it is bolded, whereas
        other rows are not.

        Returns:
              A list of lists of formatters, where the first list represents rows
              and the second columns.
        """
        bold = base.ConditionalStyle(
            style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
        )
        left_align = base.ConditionalStyle(
            style=cmi_docx.CellStyle(
                paragraph=cmi_docx.ParagraphStyle(
                    alignment=text.WD_PARAGRAPH_ALIGNMENT.LEFT
                )
            )
        )
        body_formatters = []
        for label in LANGUAGE_ROW_LABELS:
            row_formatters = []
            for col_index, width in enumerate(COLUMN_WIDTHS):
                formatter = base.Formatter(width=width)
                if col_index == 0:
                    # Test names are merged across rows.
                    formatter.merge_top = True
                if col_index == 1:
                    # Subtest rows are left-aligned
                    formatter.conditional_styles.append(left_align)
                if col_index != 0 and not label.subtest.startswith("\t"):
                    # Bold aggregate subtest rows, except the first column.
                    formatter.conditional_styles.append(bold)
                row_formatters.append(formatter)
            body_formatters.append(row_formatters)
        return body_formatters


def _get_data(mrn: str) -> sqlalchemy.Row[tuple[models.SummaryScores, models.Ctopp2]]:
    """Fetches the language data for the given mrn."""
    identifiers = utils.mrn_to_ids(mrn)
    statement = (
        sqlalchemy.select(models.SummaryScores, models.Ctopp2)
        .where(
            models.SummaryScores.person_id == identifiers.person_id,
        )
        .outerjoin(
            models.Ctopp2,
            models.Ctopp2.person_id == models.SummaryScores.person_id,
        )
    )
    with client.get_session() as session:
        data = session.execute(statement).fetchone()
    if not data:
        msg = f"Could not fetch language data for {mrn}."
        raise base.TableDataNotFoundError(msg)
    return data


class LanguageTable(
    base.WordTableSectionAddToMixin,
    base.WordTableSection,
):
    """Renderer for the language table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the langauge renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = _LanguageDataSource
