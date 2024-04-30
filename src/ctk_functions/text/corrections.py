"""Module for syntax and grammatical correctionss of text."""

import dataclasses

import mlconjug3
import spacy
from spacy import symbols, tokens

NLP = spacy.load("en_core_web_sm")
CONJUGATOR = mlconjug3.Conjugator(language="en")


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


class TextCorrections:
    """Corrects text based on the object's settings.

    Attributes:
        correct_they: Whether to correct verb conjugations associated with 'they'.
        correct_capitalization: Whether to correct the capitalization of the text
            at the start of sentences.
    """

    def __init__(
        self, *, correct_they: bool = True, correct_capitalization: bool = True
    ) -> None:
        """Initializes the TextCorrections class.

        Args:
            correct_they: Whether to correct verb conjugations associated with 'they'.
            correct_capitalization: Whether to correct the capitalization of the text.
        """
        self.correct_they = correct_they
        self.correct_capitalization = correct_capitalization

    def correct(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        paragraphs = text.split("\n")
        paragraph_text = []
        for paragraph in paragraphs:
            sentences = [sentence.text for sentence in NLP(paragraph).sents]
            paragraph_text.append(
                " ".join([self._correct_sentence(sentence) for sentence in sentences])
            )

        return "\n".join(paragraph_text)

    def _correct_they(self, sentence: str) -> str:
        subject_verb_pairs = self._find_subject_verb(sentence)
        they_verb_pairs = [
            pair for pair in subject_verb_pairs if pair.subject.lower() == "they"
        ]
        for pair in reversed(they_verb_pairs):
            sentence = self._correct_they_verb_conjugation(sentence, pair)
        return sentence

    def _correct_capitalization(self, sentence: str) -> str:
        """Corrects the capitalization of a sentence.

        Args:
            sentence: The text to correct.

        Returns:
            The corrected text.
        """
        for i, char in enumerate(sentence):
            if char.isalpha():
                return sentence[:i] + sentence[i].upper() + sentence[i + 1 :]
        return sentence

    def _correct_sentence(self, sentence: str) -> str:
        """Corrects the sentence following the object's settings.

        Args:
            sentence: The sentence to correct.

        Returns:
            The corrected sentence.
        """
        if self.correct_they:
            sentence = self._correct_they(sentence)
        if self.correct_capitalization:
            sentence = self._correct_capitalization(sentence)
        return sentence

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

        verb = CONJUGATOR.conjugate(pair.verb_token.lemma_)
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

        return (
            sentence[: pair.verb_indices[0]]
            + conjugated_verb
            + sentence[pair.verb_indices[1] :]
        )

    @staticmethod
    def _find_subject_verb(sentence: str) -> list[SubjectVerbPair]:
        """Finds the subject and verb of a sentence.

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
