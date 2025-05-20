"""Module for inserting the language table."""

import dataclasses
import functools
from typing import Literal

from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import sql_data, types
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(2.09),
    shared.Cm(6.4),
    shared.Cm(2.5),
    shared.Cm(2.62),
    shared.Cm(2.88),
)

TABLE_NAMES = Literal["SummaryScores", "Ctopp2"]


@dataclasses.dataclass
class LanguageRowLabels:
    """Definitions of the rows of the language table."""

    test: str
    subtest: str
    score_column: str | None


LANGUAGE_ROW_LABELS = (
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Listening Comprehension",
        score_column="WIAT_4_LC_Std",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="\tReceptive Vocabulary",
        score_column="WIAT_4_LC_RV_Std",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="\tOral Discourse Comprehension",
        score_column="WIAT_4_LC_ODC_Std",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Memory",
        score_column=None,
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tNon-word Repetition",
        score_column="NR_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Awareness",
        score_column="CTOPP_PA_Comp",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tElision",
        score_column="EL_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tBlending Words",
        score_column="BW_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Symbolic Naming",
        score_column="RSN_composite",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tRapid Digit Naming",
        score_column="RD_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tRapid Letter Naming",
        score_column="RL_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Non-Symbolic",
        score_column="RnSN_composite",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tRapid Object Naming",
        score_column="RO_Standard",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="\tRapid Color Naming",
        score_column="RC_standard",
    ),
)


class _LanguageDataSource(base.DataProducer):
    """Fetches the data for the Language table."""

    @classmethod
    def test_ids(cls, mrn: str) -> tuple[types.TestId, ...]:
        tests = [row[0] for row in cls.fetch(mrn)]
        test_ids: list[types.TestId] = []
        if any("ctopp" in test.lower() for test in tests):
            test_ids.append("ctopp_2")
        if any("wiat" in test.lower() for test in tests):
            test_ids.append("wiat_4")
        return tuple(test_ids)

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> tuple[tuple[str, ...], ...]:
        """Fetches the Language data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = sql_data.fetch_participant_row("person_id", mrn, models.SummaryScores)
        header = ("Test", "Subtest", "Standard Score", "Percentile", "Range")

        content_rows = [
            cls._get_content_row(data, label) for label in LANGUAGE_ROW_LABELS
        ]
        content_rows_no_none = [row for row in content_rows if row]
        return header, *content_rows_no_none

    @staticmethod
    def _get_content_row(
        data: models.SummaryScores,
        label: LanguageRowLabels,
    ) -> tuple[str, str, str, str, str] | None:
        """Gets the rows of the table's body.

        Note that rows without data are omitted, unless they are explicitly
        set to None in the labels, in which case they are included without
        content in the score/percentile/qualifier cells.

        Args:
            data: The participant's data for the SummaryScores and Ctopp2 tables.
            label: The definition of the requested row.

        Returns:
            In this order: the test cell, the subtest cell, the score cell, the
            percentile cell, and the qualifier cell.
        """
        if label.score_column and not getattr(data, label.score_column):
            # Rows without data should be omitted.
            return None

        if not label.score_column:
            # Special handling for score_column=None
            # Add an empty row; these are label rows.
            return label.test, label.subtest, "", "", ""

        score = getattr(data, label.score_column)
        percentile = (
            f"{utils.normal_score_to_percentile(float(score), mean=100, std=15):.0f}"
        )
        qualifier = utils.standard_score_to_qualifier(float(score))
        return label.test, label.subtest, f"{score:.0f}", percentile, qualifier


def _get_formatters(n_rows: int) -> tuple[tuple[base.Formatter, ...], ...]:
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
    bold_rows = (
        base.ConditionalTableStyle(
            condition=lambda table, row, _: not table.rows[row]
            .cells[1]
            .text.startswith("\t"),
            style=base.Styles.BOLD.style,
        ),
    )
    subtest_formatting = {
        (index, 1): (base.Styles.LEFT_ALIGN,) for index in range(1, n_rows)
    }
    return base.FormatProducer.produce(
        n_rows=n_rows,
        column_widths=COLUMN_WIDTHS,
        merge_top=(0,),
        cell_styles=subtest_formatting,
        table_styles=bold_rows,
    )


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
        self.formatters = _get_formatters(n_rows=len(self.data_source.fetch(mrn)))
