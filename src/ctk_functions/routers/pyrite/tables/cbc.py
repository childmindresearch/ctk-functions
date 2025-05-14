"""Module for inserting all Child Behavioral Checklist (CBC) tables."""

import dataclasses
import enum

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite import types
from ctk_functions.routers.pyrite.tables import base
from ctk_functions.routers.pyrite.tables.generic import tscore


@dataclasses.dataclass(frozen=True)
class TestDefinition:
    """Stores the model and test ids associated with a CBC test."""

    model: type[models.Base]
    test_ids: tuple[types.TestId, ...]


class CbcTests(enum.Enum):
    """All Child Behavior Checklist tests."""

    ASR = TestDefinition(model=models.Asr, test_ids=("asr",))
    CBCL = TestDefinition(model=models.Cbcl, test_ids=("cbcl",))
    TRF = TestDefinition(model=models.Trf, test_ids=("trf",))
    YSR = TestDefinition(model=models.Ysr, test_ids=("ysr",))


SUBSCALES = [
    ("Anxious/Depressed", "AD"),
    ("Withdrawn/Depressed", "WD"),
    ("Somatic Complaints", "SC"),
    ("Social Problems", "SP"),
    ("Thought Problems", "TP"),
    ("Attention Problems", "AP"),
    ("Rule Breaking Behaviors", "RBB"),
    ("Aggressive Behaviors", "AB"),
    ("Internalizing (Emotional) Problems", "Int"),
    ("Externalizing (Behavioral) Problems", "Ext"),
    ("Total Problems", "Total"),
]


# There are two sets of thresholds for clinical relevance.
# The one with higher scores is denoted as "HIGH", the other as "LOW".
CLINICAL_RELEVANCE_HIGH = [
    base.ClinicalRelevance(
        low=None,
        high=65,
        high_inclusive=False,
        label="typical range",
        style=cmi_docx.CellStyle(),
    ),
    base.ClinicalRelevance(
        low=65,
        high=70,
        low_inclusive=True,
        label="borderline range",
        style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=70,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.CellStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]

CLINICAL_RELEVANCE_LOW = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        high_inclusive=False,
        label="typical range",
        style=cmi_docx.CellStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=65,
        low_inclusive=True,
        label="borderline range",
        style=cmi_docx.CellStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=65,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.CellStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


def _create_cbc_row_label(
    test_key: CbcTests, subscale: str, suffix: str
) -> tscore.TScoreRowLabel:
    """Create a TScoreRowLabel for CBC tests.

    Args:
        test_key: The CBC test key
        subscale: The name of the subscale
        suffix: The suffix for the score column

    Returns:
        A TScoreRowLabel instance
    """
    relevance = (
        CLINICAL_RELEVANCE_LOW
        if suffix in ("Int", "Ext", "Total")
        else CLINICAL_RELEVANCE_HIGH
    )
    return tscore.TScoreRowLabel(
        subscale=subscale,
        score_column=f"{test_key.name}_{suffix}_T",
        relevance=relevance,
    )


def get_row_labels(test: CbcTests) -> tuple[tscore.TScoreRowLabel, ...]:
    """Creates the row labels.

    ASR does not have the social problems entry and requires special handling.

    Args:
        test: The CBC test

    Returns:
        The row labels associated with this test.
    """
    if test == CbcTests.ASR:
        subscales = [scale for scale in SUBSCALES if scale[0] != "Social Problems"]
    else:
        subscales = SUBSCALES

    return tuple(
        _create_cbc_row_label(test, subscale, suffix) for subscale, suffix in subscales
    )


def _create_data_table(test: CbcTests) -> type:
    """Factory for a CBC table.

    Note that the return type hint cannot be more specific as mypy does not
    support multiple inheritance.

    Args:
        test: The cognitive test to generate the table for.

    Returns:
        The renderer for a CBC table.
    """
    labels = get_row_labels(test)

    class CbcTable(base.WordTableSectionAddToMixin, base.WordTableSection):
        """Renderer for a CBC table."""

        def __init__(self, mrn: str) -> None:
            """Initializes the table renderer.

            Args:
                mrn: The participant's unique identifier.'
            """
            self.mrn = mrn
            self.data_source = tscore.create_data_producer(
                test_ids=test.value.test_ids,
                model=test.value.model,
                labels=labels,
            )
            border_index = (
                next(
                    index
                    for index, label in enumerate(labels)
                    if label.relevance == CLINICAL_RELEVANCE_LOW
                )
                + 1
            )
            self.formatters = tscore.fetch_tscore_formatters(
                labels, top_border_rows=(border_index,)
            )

    return CbcTable


CbclTable = _create_data_table(test=CbcTests.CBCL)
YsrTable = _create_data_table(test=CbcTests.YSR)
TrfTable = _create_data_table(test=CbcTests.TRF)
AsrTable = _create_data_table(test=CbcTests.ASR)
