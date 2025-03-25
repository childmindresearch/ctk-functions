"""Module for inserting the language table."""

import dataclasses

import sqlalchemy

from ctk_functions.microservices.sql import client, models
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


class LanguageDataSource(base.DataProducer):
    """Fetches the data for the Language table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the Language data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        eid = utils.mrn_to_eid(mrn)
        statement = (
            sqlalchemy.select(models.Wiat, models.Ctopp2)
            .where(
                models.Wiat.EID == eid,
            )
            .outerjoin(
                models.Ctopp2,
                models.Wiat.EID == models.Ctopp2.EID,
            )
        )

        with client.get_session() as session:
            data = session.execute(statement).fetchone()

        header = [
            base.WordTableCell(content="Test"),
            base.WordTableCell(content="Subtest"),
            base.WordTableCell(content="Standard Score"),
            base.WordTableCell(content="Percentile"),
            base.WordTableCell(content="Range"),
        ]

        content_rows = []
        for label in LANGUAGE_ROW_LABELS:
            test_cell = base.WordTableCell(
                content=label.test,
                formatter=base.Formatter(merge_top=True),
            )
            subtest_cell = base.WordTableCell(content=label.subtest)

            if label.score_column is None:
                # TODO: Remove this once the correct column is found.
                # Must set data_index, but the value doesn't matter in this case.
                data_index = 0
            else:
                data_index = int(label.score_column.startswith("CTOPP_"))

            if not label.score_column or not getattr(
                data[data_index],  # type: ignore[index]
                label.score_column,
            ):
                score_cell = base.WordTableCell(content="N/A")
                percentile_cell = base.WordTableCell(content="N/A")
                range_cell = base.WordTableCell(content="N/A")
            else:
                score = float(getattr(data[data_index], label.score_column))  # type: ignore[index]
                percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
                qualifier = utils.standard_score_to_qualifier(score)
                score_cell = base.WordTableCell(content=str(int(score)))
                percentile_cell = base.WordTableCell(content=f"{percentile:.0f}")
                range_cell = base.WordTableCell(content=qualifier)

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
