"""regex test package"""

from regex.models import Analizer

def test_sentences_count():
    analyzer = Analizer()
    analyzer.text = "One. Two. Three? Four! Five."
    analyzer.analize()
    assert analyzer.report.sentences_count == 5


def test_narrative_count():
    analyzer = Analizer()
    analyzer.text = "One. Two. Three? Four! Five."
    analyzer.analize()
    assert analyzer.report.narrative_count == 3


def test_interrogative_count():
    analyzer = Analizer()
    analyzer.text = "One. Two. Three? Four! Five."
    analyzer.analize()
    assert analyzer.report.interrogative_count == 1


def test_imperative_count():
    analyzer = Analizer()
    analyzer.text = "One. Two. Three? Four! Five."
    analyzer.analize()
    assert analyzer.report.imperative_count == 1


def test_sentence_avg_len():
    analyzer = Analizer()
    analyzer.text = "Ab. Bcd. Efgh!"
    analyzer.analize()
    assert analyzer.report.sentence_chars_avg_len == 3


def test_word_avg_len():
    analyzer = Analizer()
    analyzer.text = "Ab. Bcd. Efgh!"
    analyzer.analize()
    assert analyzer.report.word_chars_avg_len == 3


def test_emoji_count():
    analyzer = Analizer()
    analyzer.text = ":) :-( ;] :-] :( [] : -"
    analyzer.analize()
    assert analyzer.report.emoji_count == 5


def test_lower_consonant_words():
    analyzer = Analizer()
    analyzer.text = "test otest Apple best"
    analyzer.analize()
    
    words = analyzer.report.consonant_lower_words
    assert len(words) == 2
    assert "test" in words
    assert "best" in words


def test_car_numbers():
    analyzer = Analizer()
    analyzer.text = "Valid 1234 AA-1 end. Invalid 0000 AA-1. Valid 1000 AA-1. Bad 1234 AA-9. Good 5678 BB-2."
    analyzer.analize()
    
    nums = analyzer.report.car_numbers
    assert len(nums) == 3
    assert "1234 AA-1" in nums
    assert "1000 AA-1" in nums
    assert "5678 BB-2" in nums


def test_min_words_count():
    analyzer = Analizer()
    analyzer.text = "I am here, ok a."
    analyzer.analize()
    
    assert analyzer.report.min_len_words_count == 2


def test_comma_words():
    analyzer = Analizer()
    analyzer.text = "Hello, world-1, test,"
    analyzer.analize()
    
    words = analyzer.report.comma_words
    assert len(words) == 3
    assert "Hello" in words
    assert "1" in words 
    assert "test" in words


def test_max_y_word():
    analyzer = Analizer()
    analyzer.text = "Look at the Sky. It is happy by nature."
    analyzer.analize()
    
    assert analyzer.report.max_y_word == "happy"