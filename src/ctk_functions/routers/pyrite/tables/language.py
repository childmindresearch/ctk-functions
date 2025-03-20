"""Module for inserting the language table."""

import dataclasses
from typing import Any

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class LanguageRowLabels:
    """Definitions of the rows of the language table."""

    test: str
    subtest: str
    score_column: str | None
    percentile_column: str | None


LANGUAGE_ROW_LABELS = (
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Listening Comprehension",
        score_column="WIAT_LC_Stnd",
        percentile_column="WIAT_LC_P",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Receptive Vocabulary",
        score_column="WIAT_LCRV_Std",
        percentile_column="WIAT_LCRV_P",
    ),
    LanguageRowLabels(
        test="WIAT-4",
        subtest="Oral Discourse Comprehension",
        score_column="WIAT_LCODC_Stnd",
        percentile_column="WIAT_LCODC_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Memory",
        score_column=None,
        percentile_column=None,
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Non-word Repetition",
        score_column="CTOPP_NR_R",
        percentile_column="CTOPP_NR_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Phonological Awareness",
        score_column="CTOPP_PA_Comp",
        percentile_column="CTOPP_PA_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Elision",
        score_column="CTOPP_EL_R",
        percentile_column="CTOPP_EL_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Blending Words",
        score_column="CTOPP_BW_R",
        percentile_column="CTOPP_BW_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Symbolic Naming",
        score_column="CTOPP_RSN_Comp",
        percentile_column="CTOPP_RSN_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Digit Naming",
        score_column="CTOPP_RD_R",
        percentile_column="CTOPP_RD_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Letter Naming",
        score_column="CTOPP_RL_R",
        percentile_column="CTOPP_RL_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="Rapid Non-Symbolic",
        score_column="CTOPP_RnSN_Comp",
        percentile_column=None,
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Object Naming",
        score_column="CTOPP_RO_R",
        percentile_column="CTOPP_RO_P",
    ),
    LanguageRowLabels(
        test="CTOPP-2",
        subtest="- Rapid Color Naming",
        score_column=None,
        percentile_column=None,
    ),
)


class Language(base.BaseTable):
    """Fetches and creates the Langauge table."""

    _title = None

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return (
            sqlalchemy.select(models.t_I2B2_Export_WIAT_t, models.t_I2B2_Export_CTOPP_t)
            .where(
                self.eid == models.t_I2B2_Export_WIAT_t.c.EID,  # type: ignore[arg-type]
            )
            .outerjoin(
                models.t_I2B2_Export_CTOPP_t,
                models.t_I2B2_Export_WIAT_t.c.EID == models.t_I2B2_Export_CTOPP_t.c.EID,
            )
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the Language table to the report.

        Args:
            doc: The Word document.
        """
        header_texts = [
            "Test",
            "Subtest",
            "Standard Score",
            "Percentile",
            "Range",
        ]
        table = doc.add_table(len(LANGUAGE_ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)

        for index, label in enumerate(LANGUAGE_ROW_LABELS):
            index += 1  # noqa: PLW2901 # Adjust for header row.
            row = table.rows[index].cells
            utils.set_index_column_name_or_merge(
                table,
                label.test,
                row_index=index,
                col_index=0,
            )
            row[1].text = label.subtest
            if label.score_column and getattr(self.data_no_none, label.score_column):
                score = int(getattr(self.data_no_none, label.score_column))
                row[2].text = str(score) if score else "N/A"
                row[3].text = (
                    str(utils.standard_score_to_percentile(score)) if score else "N/A"
                )
                row[4].text = (
                    utils.standard_score_to_qualifier(score) if score else "N/A"
                )
            else:
                row[2].text = "N/A"
                row[3].text = "N/A"
                row[4].text = "N/A"
