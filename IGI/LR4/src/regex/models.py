"""models"""

from dataclasses import dataclass
import re


@dataclass
class Report:
    """report about input text"""
    sentences_count: int
    narrative_count: int
    interrogative_count: int
    imperative_count: int
    sentence_chars_avg_len: int
    word_chars_avg_len: int
    emoji_count: int
    consonant_lower_words: list[str]
    car_numbers: list[str]
    min_len_words_count: int
    comma_words: list[str]
    max_y_word: str

    def __str__(self):
        return f"Sentences count: {self.sentences_count}" \
            f"    Narrative count: {self.narrative_count}\n" \
            f"    Interrogative count: {self.interrogative_count}\n" \
            f"    Imperative count: {self.imperative_count}\n" \
            f"Average length of sentence: {self.sentence_chars_avg_len}\n" \
            f"Average length of word: {self.word_chars_avg_len}\n" \
            f"Emoji count: {self.emoji_count}\n" \
            f"Consonant words with lowercase begin: {self.consonant_lower_words}\n" \
            f"Car numbers: {self.car_numbers}\n" \
            f"Min length words count: {self.min_len_words_count}\n" \
            f"Words with comma: {self.comma_words}\n" \
            f"Max y-begin word: {self.max_y_word}"


class Analizer:
    """text analizer"""

    def __init__(self):
        self._text = ""
        self._report = None

    @property
    def text(self):
        """text getter"""
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def report(self) -> Report:
        """report getter"""
        return self._report

    def analize(self) -> None:
        self._report = Report(self._sentences_count(),
                            self._narrative_count(),
                            self._interrogative_count(),
                            self._imperative_count(),
                            self._sentence_chars_avg_len(),
                            self._word_chars_avg_len(),
                            self._emoji_count(),
                            self._lower_consonant_words(),
                            self._car_numbers(),
                            self._min_len_words_count(),
                            self._comma_words(),
                            self._max_y_word())

    def _sentences_count(self) -> int:
        pattern = r"[\w\s,-]+[\.\?!](?=\s|$)"
        return len(re.findall(pattern, self._text))

    def _narrative_count(self) -> int:
        pattern = r"[\w\s,-]+\.(?=\s|$)"
        return len(re.findall(pattern, self._text))

    def _interrogative_count(self) -> int:
        pattern = r"[\w\s,-]+\?(?=\s|$)"
        return len(re.findall(pattern, self._text))

    def _imperative_count(self) -> int:
        pattern =r"[\w\s,-]+!(?=\s|$)"
        return len(re.findall(pattern, self._text))

    def _sentence_chars_avg_len(self) -> int:
        lens = [len(re.findall(r"[^.\?!\s]", i.group()))
                for i in re.finditer(r"[\w\s,-]+[\.\?!](?=\s|$)", self._text)]

        if not lens:
            return 0
        return round(sum(lens) / len(lens))

    def _word_chars_avg_len(self) -> int:
        lens = [len(re.findall(r"\S", i.group()))
                for i in re.finditer(r"\w+", self._text)]

        if not lens:
            return 0
        return round(sum(lens) / len(lens))

    def _emoji_count(self) -> int:
        pattern = r"[:;]-*(?:\(+|\)+|\[+|\]+)"
        return len(re.findall(pattern, self._text))

    def _lower_consonant_words(self) -> list[str]:
        pattern = r"\b[bcdfghjklmnpqrstvwxyz]\w*\b"
        return re.findall(pattern, self._text)

    def _car_numbers(self) -> list[str]:
        pattern = r"\b(?!0000)\d{4}\s[A-Z]{2}-[1-8]\b"
        return re.findall(pattern, self._text)

    def _min_len_words_count(self) -> int:
        words = re.findall(r"\w+", self._text)
        
        if not words:
            return 0
        
        min_len = len(min(words, key=len))

        return sum(1 for w in words if len(w) == min_len)

    def _comma_words(self) -> list[str]:
        pattern = r"\b(\w+),"
        return re.findall(pattern, self._text)

    def _max_y_word(self) -> str:
        y_words = re.findall(r"\b\w*y\b", self._text, re.IGNORECASE)
        
        if not y_words:
            return ""
            
        return max(y_words, key=len)