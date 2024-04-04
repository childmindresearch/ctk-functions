"""Utilities for correcting grammar and syntax."""

import dataclasses

import cmi_docx
import docx
import mlconjug3
import spacy
from spacy import symbols, tokens

NLP = spacy.load("en_core_web_sm")


@dataclasses.dataclass()
class SubjectVerbPair:
    """A pair of a subject and a verb in a sentence."""

    sentence: str
    subject_token: tokens.Token
    verb_token: tokens.Token

    @property
    def subject(self) -> str:
        """The subject of the sentence."""
        return self.subject_token.text

    @property
    def verb(self) -> str:
        """The verb of the sentence."""
        return self.verb_token.text

    @property
    def verb_indices(self) -> tuple[int, int]:
        """The indices of the verb in the sentence."""
        return self.verb_token.idx, self.verb_token.idx + len(self.verb)


class DocumentCorrections:
    """Corrects verb conjugations associated with 'they' in a Word document."""

    def __init__(
        self,
        document: docx.Document,
        *,
        correct_they: bool = True,
    ) -> None:
        """Initializes the corrector with a document.

        Args:
            document: The docx document to correct.
            correct_they: Whether to correct verb conjugations associated with 'they'.

        """
        self.document = document
        self.conjugator = mlconjug3.Conjugator(language="en")
        self.correct_they = correct_they

    def correct(self) -> None:
        """Corrects verb conjugations associated with 'they' in the document."""
        if not self.correct_they:
            return

        for paragraph in self.document.paragraphs:
            self._correct_paragraph(paragraph)

    def _correct_paragraph(self, paragraph: docx.text.paragraph.Paragraph) -> None:
        """Corrects conjugations in a single paragraph.

        Args:
            paragraph: The paragraph to correct.
        """
        sentences = NLP(paragraph.text).sents
        for sentence in sentences:
            self._correct_sentence(sentence.text)

    def _correct_sentence(self, sentence: str) -> None:
        """Corrects the conjugation of verbs associated with they in a sentence.

        Args:
            sentence: The sentence to correct.
        """
        words = sentence.split()
        if "they" in [word.lower() for word in words]:
            subject_verb_pairs = self._find_subject_verb(sentence)
            they_verb_pairs = [
                pair for pair in subject_verb_pairs if pair.subject.lower() == "they"
            ]
            for pair in reversed(they_verb_pairs):
                sentence = self._correct_they_verb_conjugation(sentence, pair)

    def _correct_they_verb_conjugation(
        self,
        sentence: str,
        pair: SubjectVerbPair,
    ) -> str:
        """Corrects the verb conjugation associated with 'they' in a sentence.

        Args:
            sentence: The sentence to correct.
            pair: The pair of subject and verb in the sentence.

        Notes:
            To my knowledge, 'to be' is the only verb that has a different
            conjugation for third person singular/plural in the past tense. If
            other verbs are found to have different conjugations in the past
            tense, this function will need to be updated.
        """
        for child in pair.verb_token.children:
            if child.tag_ == "VBZ" and child.lemma_ in ["be", "have"]:
                pair.verb_token = child
            elif child.tag_ == "VBZ":
                child_pair = SubjectVerbPair(
                    sentence=sentence,
                    subject_token=pair.subject_token,
                    verb_token=child,
                )
                sentence = self._correct_they_verb_conjugation(sentence, child_pair)
        if pair.verb_token.tag_ != "VBZ" and not (
            pair.verb_token.tag_ == "VBD" and pair.verb_token.lemma_ == "be"
        ):
            return sentence

        verb = self.conjugator.conjugate(pair.verb_token.lemma_)
        if isinstance(verb, list):
            verb = verb[0]
        try:
            if pair.verb_token.tag_ == "VBZ":
                conjugated_verb = verb["indicative"]["indicative present"]["they"]  # type: ignore[index]
            else:
                conjugated_verb = verb["indicative"]["indicative past tense"]["they"]  # type: ignore[index]
        except TypeError as exc_info:
            if "'NoneType' object is not subscriptable" in str(exc_info):
                # Verb is unknown to the conjugator.
                return sentence
            raise

        new_sentence = (
            sentence[: pair.verb_indices[0]]
            + conjugated_verb
            + sentence[pair.verb_indices[1] :]
        )

        cmi_docx.ExtendDocument(self.document).replace(sentence, new_sentence)
        return new_sentence

    @staticmethod
    def _find_subject_verb(sentence: str) -> list[SubjectVerbPair]:
        """Finds the subject and verb of a sentence, only if the subject.

        Args:
            sentence: The sentence to analyze.

        Returns:
            A list of indices of subjects and verbs
        """
        doc = NLP(sentence)
        return [
            SubjectVerbPair(
                sentence=sentence,
                subject_token=word,
                verb_token=word.head,
            )
            for word in doc
            if word.dep in [symbols.nsubj, symbols.nsubjpass]
            and word.head.tag_.startswith("VB")
        ]
