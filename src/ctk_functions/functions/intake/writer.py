"""Contains report writing functionality for intake information."""

import asyncio
import dataclasses
import enum
import itertools
import pathlib
import queue
import tempfile
import uuid
from typing import AsyncGenerator, Awaitable

import cmi_docx
import docx
from docx import document as docx_document
from docx.enum import table as enum_table
from docx.enum import text as enum_text
from docx.text import paragraph as docx_paragraph

from ctk_functions import config
from ctk_functions.functions.intake import descriptors, llm, parser
from ctk_functions.functions.intake.utils import (
    language_utils,
    string_utils,
)
from ctk_functions.microservices import azure

settings = config.get_settings()
DATA_DIR = settings.DATA_DIR
AZURE_BLOB_CONNECTION_STRING = settings.AZURE_BLOB_CONNECTION_STRING
RGB_INTAKE = (178, 161, 199)
RGB_TESTING = (155, 187, 89)
RGB_TEMPLATE = (247, 150, 70)
RGB_LLM = (0, 0, 255)
PLACEHOLDER = "______"

logger = config.get_logger()


class Style(enum.Enum):
    """The styles for the report."""

    HEADING_1 = "Heading 1"
    HEADING_2 = "Heading 2"
    HEADING_3 = "Heading 3"
    TITLE = "Title"
    NORMAL = "Normal"


@dataclasses.dataclass
class Image:
    """Represents an image to be inserted into the report.

    Attributes:
        name: The name of the image.
        binary_data: The binary data representing the image.
    """

    name: str
    binary_data: bytes


@dataclasses.dataclass
class LlmPlaceholder:
    """Represents a placeholder for large language model input in the report.

    Attributes:
        id: The unique identifier for the placeholder. Will be inserted into
            the report as {{id}}.
        replacement: The replacement text for the placeholder.
    """

    id: str
    replacement: Awaitable[str]


class ReportWriter:
    """Writes a report for intake information."""

    def __init__(self, intake: parser.IntakeInformation) -> None:
        """Initializes the report writer.

        Args:
            intake: The intake information.
        """
        logger.debug("Initializing the report writer.")
        self.intake = intake
        self.report: docx_document.Document = docx.Document(
            DATA_DIR / "report_template.docx"
        )
        self.insert_before = next(
            paragraph
            for paragraph in self.report.paragraphs
            if "MENTAL STATUS EXAMINATION AND TESTING BEHAVIORAL OBSERVATIONS"
            in paragraph.text
        )
        self.llm_placeholders: queue.SimpleQueue[LlmPlaceholder] = queue.SimpleQueue()

        if not self.insert_before:
            msg = "Insertion point not found in the report template."
            raise ValueError(msg)

    async def transform(self) -> None:
        """Transforms the intake information to a report."""
        logger.debug("Transforming the intake information to a report.")

        self.write_reason_for_visit()
        self.write_developmental_history()
        self.write_academic_history()
        self.write_social_history()
        self.write_psychiatric_history()
        self.write_medical_history()
        self.write_current_psychiatric_functioning()
        self.add_page_break()

        self.replace_patient_information()
        self.apply_corrections()
        await self.add_signatures()
        await self.make_llm_edits()

    def replace_patient_information(self) -> None:
        """Replaces the patient information in the report."""
        logger.debug("Replacing patient information in the report.")
        replacements = {
            "full_name": self.intake.patient.full_name,
            "preferred_name": self.intake.patient.first_name,
            "date_of_birth": self.intake.patient.date_of_birth.strftime("%m/%d/%Y"),
            "reporting_guardian": self.intake.patient.guardian.title_name,
            "aged_gender": self.intake.patient.age_gender_label,
            "pronoun_0": self.intake.patient.pronouns[0],
            "pronoun_1": self.intake.patient.pronouns[1],
            "pronoun_2": self.intake.patient.pronouns[2],
            "pronoun_4": self.intake.patient.pronouns[4],
            "placeholder": PLACEHOLDER,
        }

        extendedDocument = cmi_docx.ExtendDocument(self.report)
        for template, replacement in replacements.items():
            template_formatted = "{{" + template.upper() + "}}"
            extendedDocument.replace(template_formatted, replacement)

    def write_reason_for_visit(self) -> None:
        """Writes the reason for visit to the end of the report."""
        logger.debug("Writing the reason for visit to the report.")
        patient = self.intake.patient
        handedness = patient.handedness
        iep = patient.education.individualized_educational_program
        past_diagnoses = patient.psychiatric_history.past_diagnoses.transform(
            short=True,
        )
        classroom = patient.education.classroom_type
        age_determinant = "an" if patient.age in (8, 18) else "a"

        concerns_id = self._create_llm_placeholder(
            excerpt=(
                f"{patient.guardian.title_full_name}, attended the present"
                + f"evaluation due to concerns regarding {PLACEHOLDER}."
            ),
            parent_input=patient.reason_for_visit,  # type: ignore[attr-defined]
        )
        hopes_id = self._create_llm_placeholder(
            excerpt=f"The family is hoping for {PLACEHOLDER}.",
            parent_input=patient.hopes,  # type: ignore[attr-defined]
        )
        learned_of_study_id = self._create_llm_placeholder(
            excerpt=f"The family learned of the study through {PLACEHOLDER}.",
            parent_input=patient.learned_of_study,  # type: ignore[attr-defined]
        )

        if patient.education.grade.isnumeric():
            grade_superscript = string_utils.ordinal_suffix(
                int(patient.education.grade),
            )
        else:
            grade_superscript = ""

        texts = [
            f"""
            At the time of enrollment, {patient.first_name} was {age_determinant}
            {patient.age}-year-old, {handedness} {patient.age_gender_label}
            {past_diagnoses}. {patient.first_name} was placed in a {classroom}
            {patient.education.grade}""",
            f"{grade_superscript} ",
            f"""
            grade classroom at {patient.education.school_name}.
            {patient.first_name} {iep}. {patient.first_name} and
            {patient.pronouns[2]} {patient.guardian.relationship},
            {concerns_id} {hopes_id} {learned_of_study_id}
        """,
        ]
        texts = [string_utils.remove_excess_whitespace(text) for text in texts]

        heading = self._insert("REASON FOR VISIT", Style.HEADING_1)
        paragraph = self._insert(texts[0])
        paragraph.add_run(texts[1]).font.superscript = True
        paragraph.add_run(" " + texts[2])
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_developmental_history(self) -> None:
        """Writes the developmental history to the end of the report."""
        logger.debug("Writing the developmental history to the report.")
        heading = self._insert("DEVELOPMENTAL HISTORY", Style.HEADING_1)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        self.write_prenatal_history()
        self.write_developmental_milestones()
        self.write_early_education()

    def write_prenatal_history(self) -> None:
        """Writes the prenatal and birth history of the patient to the report."""
        logger.debug("Writing the prenatal history to the report.")
        patient = self.intake.patient
        development = patient.development
        pregnancy_symptoms = development.birth_complications
        delivery = development.delivery
        delivery_location = development.delivery_location
        adaptability = development.adaptability
        duration_of_pregnancy = development.duration_of_pregnancy

        text = f"""
            {patient.guardian.title_name} reported {pregnancy_symptoms}.
            {patient.first_name} was born at
            {duration_of_pregnancy} of gestation with {delivery} at
            {delivery_location}. {patient.first_name} had {adaptability}
            during infancy and was {development.soothing_difficulty.name} to
            soothe.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Prenatal and Birth History", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_developmental_milestones(self) -> None:
        """Writes the developmental milestones to the report."""
        logger.debug("Writing the developmental milestones to the report.")
        patient = self.intake.patient
        started_walking = patient.development.started_walking
        started_talking = patient.development.started_talking
        daytime_dryness = patient.development.daytime_dryness
        nighttime_dryness = patient.development.nighttime_dryness

        text = f"""
            {patient.first_name}'s achievement of social, language, fine and
            gross motor developmental milestones were within normal limits, as
            reported by {patient.guardian.title_name}. {patient.first_name}
            {started_walking} and {started_talking}.
            {patient.pronouns[0].capitalize()} {daytime_dryness} and
            {nighttime_dryness}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Developmental Milestones", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_TEMPLATE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TEMPLATE)

    def write_early_education(self) -> None:
        """Writes the early education information to the report."""
        logger.debug("Writing the early education information to the report.")
        patient = self.intake.patient
        development = patient.development

        reporting_guardian = patient.guardian.title_name
        early_intervention = development.early_intervention_age
        cpse = development.cpse_age

        text = f"""
            {reporting_guardian} reported that
            {patient.first_name} {early_intervention} and {cpse}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Early Educational Interventions", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_academic_history(self) -> None:
        """Writes the academic history to the end of the report."""
        logger.debug("Writing the academic history to the report.")
        heading = self._insert("ACADEMIC AND EDUCATIONAL HISTORY", Style.HEADING_1)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        self.write_previous_testing()
        self.write_academic_history_table()
        self.write_educational_history()

    def write_previous_testing(self) -> None:
        """Writes the previous testing information to the report."""
        logger.debug("Writing the previous testing information to the report.")
        patient = self.intake.patient

        text = f"""
        {patient.first_name} has no history of previous psychoeducational
        evaluations./{patient.first_name} was evaluated by {PLACEHOLDER} in 20XX.
        Documentation of the results of the evaluation(s) were unavailable at
        the time of writing this report/ Notable results include:
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Previous Testing", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_academic_history_table(self) -> None:
        """Writes the academic history table to the report."""
        logger.debug("Writing the academic history table to the report.")
        paragraph = self._insert("Name, Date of Assessment")
        cmi_docx.ExtendParagraph(paragraph).format(
            font_rgb=RGB_INTAKE,
            bold=True,
            alignment=enum_text.WD_PARAGRAPH_ALIGNMENT.CENTER,
        )

        table = self.report.add_table(7, 4)
        self.insert_before._p.addprevious(table._tbl)  # noqa: SLF001
        table.style = "Table Grid"
        header_row = table.rows[0].cells

        header_texts = [
            "Domain/Index/Subtest",
            "Standard Score",
            "Percentile Rank",
            "Descriptor",
        ]
        for i, header in enumerate(header_texts):
            header_row[i].text = header
            header_row[i].width = 10
            cmi_docx.ExtendCell(header_row[i]).format(
                bold=True,
                font_rgb=RGB_INTAKE,
                background_rgb=(217, 217, 217),
                alignment=enum_text.WD_ALIGN_PARAGRAPH.CENTER,
            )
        for row in table.rows:
            row.height = 1
            row.height_rule = enum_table.WD_ROW_HEIGHT_RULE.EXACTLY
            for cell in row.cells:
                cmi_docx.ExtendCell(cell).format(
                    line_spacing=1,
                    space_after=0,
                    space_before=0,
                )

    def write_educational_history(self) -> None:
        """Writes the educational history to the report."""
        logger.debug("Writing the educational history to the report.")
        patient = self.intake.patient
        education = patient.education
        has_iep = (
            education.individualized_educational_program.base
            == descriptors.IndividualizedEducationProgram.yes.value
        )

        if has_iep:
            iep_prior_text = f"""
                {patient.first_name} was
                granted an Individualized Education Program (IEP) in
                {PLACEHOLDER} grade due to {PLACEHOLDER}
                difficulties.
            """
        else:
            iep_prior_text = f"""{patient.first_name} has never had an
                              Individualized Education Program (IEP)."""
        if education.grade.isnumeric():
            grade_superscript = string_utils.ordinal_suffix(education.grade)
        else:
            grade_superscript = ""
        past_schools = education.past_schools

        text_prior = f"""
            {patient.first_name} {past_schools}. {patient.pronouns[0].capitalize()}
            previously struggled with (provide details of academic challenges
            and behavioral difficulties in school). {iep_prior_text}
        """
        texts_current = [
            f"""{patient.first_name} is currently in the {education.grade}""",
            f"{grade_superscript} ",
            f"""
                grade at {education.school_name}.
                {patient.first_name} does/does not receive special
                education services and maintains/does not have an IEP
                allowing accommodations for/including {PLACEHOLDER}.
                {patient.first_name} is generally an average/above
                average/below average student and receives mostly (describe
                grades). [Describe any academic issues reported by parent or
                child.] {patient.first_name} continues to exhibit
                weaknesses in {PLACEHOLDER}.
            """,
        ]
        text_prior = string_utils.remove_excess_whitespace(text_prior)
        texts_current = [
            string_utils.remove_excess_whitespace(text) for text in texts_current
        ]

        heading = self._insert("Educational History", Style.HEADING_2)
        prior_paragraph = self._insert(text_prior)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(prior_paragraph).format(font_rgb=RGB_INTAKE)

        current_paragraph = self._insert(texts_current[0])
        current_paragraph.add_run(texts_current[1]).font.superscript = True
        current_paragraph.add_run(" " + texts_current[2])
        cmi_docx.ExtendParagraph(current_paragraph).format(font_rgb=RGB_INTAKE)

    def write_social_history(self) -> None:
        """Writes the social history to the end of the report."""
        logger.debug("Writing the social history to the report.")
        heading = self._insert("SOCIAL HISTORY", Style.HEADING_1)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        self.write_home_and_adaptive_functioning()
        self.write_social_functioning()

    def write_home_and_adaptive_functioning(self) -> None:
        """Writes the home and adaptive functioning to the report."""
        logger.debug("Writing the home and adaptive functioning to the report.")
        patient = self.intake.patient
        household = patient.household
        language_fluencies = self._join_patient_languages(self.intake.patient.languages)

        text_home = f"""
            {patient.first_name} lives in {household.city},
            {household.state}, with {household.members}.
            The {patient.guardian.parent_or_guardian}s are
            {household.guardian_marital_status}.
            {string_utils.join_with_oxford_comma(household.languages)} {"are" if
            len(household.languages) > 1 else "is"} spoken at home.
            {patient.language_spoken_best} is reportedly
            {patient.first_name}'s preferred language.
            {patient.first_name} {language_fluencies}.
        """

        text_adaptive = f"""
            {patient.guardian.title_name} denied any concerns with {patient.pronouns[2]}
            functioning in the home setting// Per {patient.guardian.title_name},
            {patient.first_name} has a history of {PLACEHOLDER} (temper
            outbursts, oppositional behaviors, etc.) in the home setting. (Write
            details of behavioral difficulties). (Also include any history of
            sleep difficulties, daily living skills, poor hygiene, etc.)
            """
        text_home = string_utils.remove_excess_whitespace(text_home)
        text_adaptive = string_utils.remove_excess_whitespace(text_adaptive)

        heading = self._insert("Home and Adaptive Functioning", Style.HEADING_2)
        home_paragraph = self._insert(text_home)
        adaptive_paragraph = self._insert(text_adaptive)

        for paragraph in (heading, home_paragraph, adaptive_paragraph):
            cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_social_functioning(self) -> None:
        """Writes the social functioning to the report."""
        logger.debug("Writing the social functioning to the report.")
        patient = self.intake.patient
        hobbies_id = self._create_llm_placeholder(
            excerpt=f"{patient.first_name}'s hobbies include {PLACEHOLDER}.",
            parent_input=patient.hobbies,  # type: ignore[attr-defined]
        )

        text = f"""
            {patient.guardian.title_name} was pleased to describe
            {patient.first_name} as a (insert adjective e.g., affectionate)
            {patient.age_gender_label}. {patient.guardian.title_name} reported
            that {patient.pronouns[0]} has many/several/one friends in
            {patient.pronouns[2]} peer group in school and on
            {patient.pronouns[2]} team/club/etc. {patient.first_name}
            socializes with friends outside of school and has a
            (positive/fair/poor) relationship with them.
            {hobbies_id}
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Social Functioning", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_psychiatric_history(self) -> None:
        """Writes the psychiatric history to the end of the report."""
        logger.debug("Writing the psychiatric history to the report.")
        heading = self._insert("PSYCHRIATIC HISTORY", Style.HEADING_1)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        self.write_past_psychriatic_diagnoses()
        self.write_past_psychiatric_hospitalizations()
        self.write_past_therapeutic_interventions()
        self.write_past_self_injurious_behaviors_and_suicidality()
        self.write_past_aggressive_behaviors_and_homicidality()
        self.exposure_to_violence_and_trauma()
        self.administration_for_childrens_services_involvement()
        self.write_family_psychiatric_history()

    def write_past_psychiatric_hospitalizations(self) -> None:
        """Writes the past psychiatric hospitalizations to the report."""
        logger.debug("Writing the past psychiatric hospitalizations to the report.")
        patient = self.intake.patient
        text = f"""
            {patient.guardian.title_name} denied any history of past psychiatric
            hospitalizations for {patient.first_name}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Past Psychiatric Hospitalizations", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_TEMPLATE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TEMPLATE)

    def administration_for_childrens_services_involvement(self) -> None:
        """Writes the ACS involvement to the report."""
        logger.debug("Writing the ACS involvement to the report.")
        patient = self.intake.patient

        text = str(patient.psychiatric_history.children_services)
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert(
            "Administration for Children's Services (ACS) Involvement",
            Style.HEADING_2,
        )
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_past_aggressive_behaviors_and_homicidality(self) -> None:
        """Writes the past aggressive behaviors and homicidality to the report."""
        logger.debug(
            "Writing the past aggressive behaviors and homicidality to the report."
        )
        patient = self.intake.patient

        text = str(patient.psychiatric_history.aggresive_behaviors)
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert(
            "Past Severe Aggressive Behaviors and Homicidality",
            Style.HEADING_2,
        )
        report = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(report).format(font_rgb=RGB_INTAKE)

    def write_past_psychriatic_diagnoses(self) -> None:
        """Writes the past psychiatric diagnoses to the report."""
        logger.debug("Writing the past psychiatric diagnoses to the report.")
        patient = self.intake.patient
        past_diagnoses = patient.psychiatric_history.past_diagnoses.transform(
            short=False,
        )

        text = f"""
            {patient.first_name} {past_diagnoses}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Past Psychiatric Diagnoses", Style.HEADING_2)
        report = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(report).format(font_rgb=RGB_INTAKE)

    def write_family_psychiatric_history(self) -> None:
        """Writes the family psychiatric history to the report."""
        logger.debug("Writing the family psychiatric history to the report.")
        patient = self.intake.patient
        text = f"""
        {patient.first_name}'s family history is largely unremarkable for
        psychiatric illnesses. {patient.guardian.title_name} denied any family
        history related to homicidality, suicidality, depression, bipolar
        disorder, attention-deficit/hyperactivity disorder, autism spectrum
        disorder, learning disorders, psychotic disorders, eating disorders,
        oppositional defiant or conduct disorders, substance abuse, panic,
        generalized anxiety, or obsessive-compulsive disorders. Information
        regarding {patient.first_name}'s family psychiatric history was
        deferred."""
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Family Psychiatric History", Style.HEADING_2)
        report = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_TEMPLATE)
        cmi_docx.ExtendParagraph(report).format(font_rgb=RGB_TEMPLATE)

    def write_past_therapeutic_interventions(self) -> None:
        """Writes the past therapeutic history to the report."""
        logger.debug("Writing the past therapeutic history to the report.")
        patient = self.intake.patient
        guardian = patient.guardian
        interventions = patient.psychiatric_history.therapeutic_interventions

        if not interventions:
            texts = [
                f"""
                    {patient.guardian.title_name} denied any history of therapeutic
                    interventions.
                """,
            ]
        else:
            texts = [
                f"""
                    From {intervention.start}-{intervention.end},
                    {patient.first_name} engaged in therapy with
                    {intervention.therapist} due to "{intervention.reason}" at a
                    frequency of {intervention.frequency}. {guardian.title_name}
                    described the treatment as "{intervention.effectiveness}".
                    Treatment was ended due to "{intervention.reason_ended}".
                    """
                for intervention in interventions
            ]

        texts = [string_utils.remove_excess_whitespace(text) for text in texts]

        heading = self._insert("Past Therapeutic Interventions", Style.HEADING_2)
        paragraphs = [self._insert(text) for text in texts]
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        for paragraph in paragraphs:
            cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_past_self_injurious_behaviors_and_suicidality(self) -> None:
        """Writes the past self-injurious behaviors and suicidality to the report."""
        logger.debug(
            "Writing the past self-injurious behaviors and suicidality to the report."
        )
        patient = self.intake.patient

        text = str(patient.psychiatric_history.self_harm)
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert(
            "Past Self-Injurious Behaviors and Suicidality",
            Style.HEADING_2,
        )
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def exposure_to_violence_and_trauma(self) -> None:
        """Writes the exposure to violence and trauma to the report."""
        logger.debug("Writing the exposure to violence and trauma to the report.")
        patient = self.intake.patient

        text = str(patient.psychiatric_history.violence_and_trauma)
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Exposure to Violence and Trauma", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_medical_history(self) -> None:
        """Writes the medical history to the end of the report."""
        logger.debug("Writing the medical history to the report.")
        patient = self.intake.patient
        primary_care = patient.primary_care

        text = f"""
            {patient.first_name}'s medical history is unremarkable for
            significant medical conditions. {patient.pronouns[0].capitalize()} is not
            currently taking any medications for chronic medical conditions.
            {primary_care.glasses_hearing_device.transform()}.
            {primary_care.prior_diseases.transform()}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("MEDICAL HISTORY", Style.HEADING_1)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_TEMPLATE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TEMPLATE)

    def write_clinical_summary_and_impressions(self) -> None:
        """Writes the clinical summary and impressions to the report."""
        logger.debug("Writing the clinical summary and impressions to the report.")
        patient = self.intake.patient
        gender = patient.age_gender_label

        text = f"""
            {patient.first_name} is a
            sociable/resourceful/pleasant/hardworking/etc. {gender} who
            participated in the Healthy Brain Network research project through
            the Child Mind Institute in the interest of participating in
            research/due to parental concerns regarding {PLACEHOLDER}.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("CLINICAL SUMMARY AND IMPRESSIONS", Style.HEADING_1)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_TESTING)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TESTING)

    def write_current_psychiatric_functioning(self) -> None:
        """Writes the current psychiatric functioning to the report.

        Note: this section mixes color codings. Color decorators are applied
        to the called functions instead.
        """
        logger.debug("Writing the current psychiatric functioning to the report.")
        heading = self._insert("CURRENT PSYCHIATRIC FUNCTIONING", Style.HEADING_1)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        self.write_current_psychiatric_medications_intake()
        self.write_current_psychiatric_medications_testing()
        self.write_denied_symptoms()

    def write_current_psychiatric_medications_intake(self) -> None:
        """Writes the current psychiatric medications to the report."""
        logger.debug("Writing the current psychiatric medications to the report.")
        patient = self.intake.patient
        text = f"""
            {patient.first_name} is currently prescribed a daily/twice daily
            oral course of {PLACEHOLDER} for {PLACEHOLDER}.
            {patient.pronouns[0].capitalize()} is being treated by Doctortype,
            DoctorName, monthly/weekly/biweekly. The medication has been
            ineffective/effective.
        """
        text = string_utils.remove_excess_whitespace(text)

        heading = self._insert("Current Psychiatric Medications", Style.HEADING_2)
        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(heading).format(font_rgb=RGB_INTAKE)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_INTAKE)

    def write_current_psychiatric_medications_testing(self) -> None:
        """Writes the current psychiatric medications to the report."""
        logger.debug("Writing the current psychiatric medications to the report.")
        patient = self.intake.patient
        texts = [
            f"""
        [Rule out presenting diagnoses, using headlines and KSADS/DSM criteria.
        Examples of headlines include: Temper Outbursts (ending should include
        “{patient.guardian.title_name} denied any consistent patterns of
        irritability for {patient.first_name}" if applicable), Inattention
        and Hyperactivity, Autism-Related Symptoms, Oppositional Defiant
        Behaviors, etc.].""",
            "Establish a baseline first for temper outbursts",
            f"""
           (Ex:
        Though {patient.first_name} is generally a {PLACEHOLDER} child,
        {patient.pronouns[0]} continues to have difficulties with temper
        tantrums…).
        """,
        ]
        texts = [string_utils.remove_excess_whitespace(text) for text in texts]

        paragraph = self._insert(texts[0])
        paragraph.add_run(texts[1])
        paragraph.runs[-1].bold = True
        paragraph.add_run(texts[2])
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TESTING, italics=True)

    def write_denied_symptoms(self) -> None:
        """Writes the denied symptoms to the report."""
        logger.debug("Writing the denied symptoms to the report.")
        patient = self.intake.patient
        text = f"""
        {patient.guardian.title_name} and {patient.first_name} denied any
        current significant symptoms related to mood, suicidality, psychosis,
        eating, oppositional or conduct behaviors, substance abuse, autism,
        tics, inattention/hyperactivity, enuresis/encopresis, trauma, sleep,
        panic, anxiety or obsessive-compulsive disorders.
        """
        text = string_utils.remove_excess_whitespace(text)

        paragraph = self._insert(text)
        cmi_docx.ExtendParagraph(paragraph).format(font_rgb=RGB_TESTING)

    def apply_corrections(self) -> None:
        """Applies various grammatical and styling corrections."""
        logger.debug("Applying corrections to the report.")
        document_corrector = language_utils.DocumentCorrections(self.report)
        document_corrector.correct()

    async def add_signatures(self) -> None:
        """Adds the signatures to the report.

        Michael Milham's signature is placed in a different location than the
        other signatures. As such, it needs some custom handling.
        """
        logger.debug("Adding signatures to the report.")
        signatures = self._download_signatures()
        async for signature in signatures:
            paragraph_index = next(
                index
                for index in range(len(self.report.paragraphs))
                if self.report.paragraphs[index].text.lower().startswith(signature.name)
            )

            if signature.name != "michael p. milham":
                paragraph_index -= 1
            self._insert_image(paragraph_index, signature)

            if signature.name != "michael p. milham":
                cmi_docx.ExtendDocument(self.report)._insert_empty_paragraph(
                    paragraph_index
                )

    async def make_llm_edits(self) -> None:
        """Makes edits to the report using a large language model."""
        logger.debug("Making edits to the report using a large language model.")
        extendedDocument = cmi_docx.ExtendDocument(self.report)
        while not self.llm_placeholders.qsize() == 0:
            placeholder = self.llm_placeholders.get()
            new_text = await placeholder.replacement
            extendedDocument.replace(
                "{{" + placeholder.id + "}}", new_text, {"font_rgb": RGB_LLM}
            )

    def _insert_image(self, paragraph_index: int, image: Image) -> None:
        """Inserts an image into the report."""
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = pathlib.Path(temp_dir) / f"{image.name}.png"
            with image_path.open("wb") as file:
                file.write(image.binary_data)
            cmi_docx.ExtendDocument(self.report).insert_image(
                paragraph_index, image_path
            )

    def add_page_break(self) -> None:
        """Adds a page break to the report."""
        paragraph = self._insert("")
        paragraph.add_run().add_break(enum_text.WD_BREAK.PAGE)

    def _insert(
        self,
        text: str,
        style: Style = Style.NORMAL,
    ) -> docx_paragraph.Paragraph:
        """Inserts text at the insertion point.

        Given the current structure of the report, text insertions only occur
        in one location.

        Args:
            text: The text to insert.
            style: The style of the text.

        Returns:
            The new paragraph.
        """
        insertion_index = next(
            index
            for index in range(len(self.report.paragraphs))
            if self.report.paragraphs[index].text == self.insert_before.text
        )
        return cmi_docx.ExtendDocument(self.report).insert_paragraph_by_text(
            insertion_index, text, style.value
        )

    @staticmethod
    def _join_patient_languages(languages: list[parser.Language]) -> str:
        """Joins the patient's languages."""
        fluency_groups = itertools.groupby(
            languages,
            key=lambda language: language.fluency,
        )
        fluency_dict = {
            fluency: [language.name for language in language_group]
            for fluency, language_group in fluency_groups
        }

        language_descriptions = [
            f"{fluency} in {string_utils.join_with_oxford_comma(fluency_dict[fluency])}"
            for fluency in ["fluent", "proficient", "conversational"]
            if fluency in fluency_dict
        ]
        prepend_is = len(language_descriptions) > 0
        if "basic" in fluency_dict:
            language_descriptions.append(
                (
                    "has basic skills in "
                    f"{string_utils.join_with_oxford_comma(fluency_dict['basic'])}"
                ),
            )

        text = string_utils.join_with_oxford_comma(language_descriptions)
        if prepend_is:
            text = "is " + text
        return text

    @staticmethod
    async def _download_signatures() -> AsyncGenerator[Image, None]:
        """Downloads signatures from Azure blob storage.

        Returns:
            Bytes of the downloaded signatures.
        """
        azure_blob_service = azure.AzureBlobService(
            AZURE_BLOB_CONNECTION_STRING.get_secret_value()
        )
        container_contents = await azure_blob_service.directory_contents(
            "ctk-functions"
        )
        signature_filepaths = [
            content
            for content in container_contents
            if content.startswith("signatures")
        ]
        signature_promises = [
            azure_blob_service.download_blob("ctk-functions", signature)
            for signature in signature_filepaths
        ]
        signature_bytes = await asyncio.gather(*signature_promises)
        await azure_blob_service.close()
        for filepath, binary_data in zip(signature_filepaths, signature_bytes):
            person_name = (
                ".".join(filepath.split("/")[-1].split(".")[0:-1])
                .lower()
                .replace("_", " ")
            )
            yield Image(person_name, binary_data)

    def _create_llm_placeholder(self, excerpt: str, parent_input: str) -> str:
        """Stores a placeholder that will later be editted by a large language model.

        Args:
            excerpt: The excerpt to provide to the large language model.
            parent_input: The parent input that need be incorporated in the excerpt.
        """
        id = str(uuid.uuid4())
        replacement = llm.LlmEditor().run(excerpt, parent_input, PLACEHOLDER)
        self.llm_placeholders.put(LlmPlaceholder(id, replacement))
        return f"{{{{{id}}}}}"
