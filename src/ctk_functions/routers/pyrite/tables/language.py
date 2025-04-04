"""Module for inserting the language table."""

import dataclasses
import functools
from typing import Literal

import sqlalchemy
from docx import shared

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (
    shared.Cm(1.98),
    shared.Cm(5.75),
    shared.Cm(3.25),
    shared.Cm(2.21),
    shared.Cm(3.29),
)


@dataclasses.dataclass
class LanguageRowLabels:
    """Definitions of the rows of the language table."""

    test: str
    subtest: str
    score_column: str | None
    table: Literal["SummaryScores", "Ctopp2"]


LANGUAGE_ROW_LABELS = (
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Listening Comprehension",
        score_column="WIAT_4_LC_Std",
        table="SummaryScores",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Receptive Vocabulary",
        score_column="WIAT_4_LC_RV_Std",
        table="SummaryScores",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Oral Discourse Comprehension",
        score_column="WIAT_4_LC_ODC_Std",
        table="SummaryScores",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Memory",
        score_column=None,
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Non-word Repetition",
        score_column="NR_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Awareness",
        score_column="CTOPP_PA_Comp",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Elision",
        score_column="EL_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Blending Words",
        score_column="BW_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Symbolic Naming",
        score_column="RSN_composite",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Digit Naming",
        score_column="RD_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Letter Naming",
        score_column="RL_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Non-Symbolic",
        score_column="RnSN",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Object Naming",
        score_column="RO_Standard",
        table="Ctopp2",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Color Naming",
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

        body_formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        body_formatters[0].merge_top = True
        content_rows = []
        for label in LANGUAGE_ROW_LABELS:
            test_cell = base.WordTableCell(
                content=label.test,
                formatter=body_formatters[0],
            )
            subtest_cell = base.WordTableCell(
                content=label.subtest, formatter=body_formatters[1]
            )
            data_table = data[int(label.table == "Ctopp2")]
            if not label.score_column or not getattr(data_table, label.score_column):
                score_cell = base.WordTableCell(
                    content="N/A", formatter=body_formatters[2]
                )
                percentile_cell = base.WordTableCell(
                    content="N/A", formatter=body_formatters[3]
                )
                range_cell = base.WordTableCell(
                    content="N/A", formatter=body_formatters[4]
                )
            else:
                score = float(getattr(data_table, label.score_column))
                percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
                qualifier = utils.standard_score_to_qualifier(score)
                score_cell = base.WordTableCell(
                    content=str(int(score)), formatter=body_formatters[2]
                )
                percentile_cell = base.WordTableCell(
                    content=f"{percentile:.0f}", formatter=body_formatters[3]
                )
                range_cell = base.WordTableCell(
                    content=qualifier, formatter=body_formatters[4]
                )

            content_rows.append(
                [
                    test_cell,
                    subtest_cell,
                    score_cell,
                    percentile_cell,
                    range_cell,
                ],
            )

        return base.WordTableMarkup(rows=[header, *content_rows])


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
        raise utils.TableDataNotFoundError(msg)
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
