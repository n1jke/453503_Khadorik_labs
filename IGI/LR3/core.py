"""
Task 1-5:
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Version: 1.0
"""

import math
import string as strlib

from exceptions import InvalidDomainError, ConvergenceError, EmptySequenceError

MAX_ITERATIONS_SERIES = 500

def task_1(x: float, eps: float) -> tuple[int, float, float]:
    """
    Calculate ln((x+1)/(x-1)) using series expansion.
    Series: 2 * sum(1/((2n+1)*x^(2n+1))) for n=0...inf.

    Args:
        x: arg value (|x| > 1)
        eps: precision

    Returns:
        tuple: (n_iterations, math_reference_value, series_calculated_value)

    Raises:
        InvalidDomainError: If |x| <= 1
        ConvergenceError: If series doesn't converge in MAX_ITERATIONS
    """

    if math.fabs(x) <= 1:
        raise InvalidDomainError(f"Domain error: |x| must be > 1, got {x}")

    target = math.log((x + 1) / (x-1))
    series = 0.0

    for n in range(MAX_ITERATIONS_SERIES):
        term = 2.0 / ((2 * n + 1) * math.pow(x, 2 * n + 1))
        series += term
        if math.fabs(term) < eps:
            return n + 1, target, series

    raise ConvergenceError(
        f"Series did not converge in {MAX_ITERATIONS_SERIES} iterations"
    )


def task_2(array: list[int]) -> tuple[float, int, list[int]]:
    """
    Calculates average of even numbers from given list.

    Returns:
        tuple: (average, count_of_even_numbers, list_of_even_numbers)

    Raises:
        EmptySequenceError: If even numbers not found
    """

    evens = [item for item in array if item % 2 == 0]
    if not evens:
        raise EmptySequenceError("No even numbers found in sequence")
    avg = sum(evens) / len(evens)
    return avg, len(evens), evens

def task_3(string: str) -> int:
    """
     Task 3: Count words starting with lowercase letter.

     Args:
         string: Input string

     Returns:
         Count of words starting with lowercase letter
     """

    words = string.split()
    n = 0
    for word in words:
        clean = word.strip(strlib.punctuation)
        if clean and clean[0].islower():
            n += 1

    return n

def task_4(string: str = None) -> tuple[int, int, int, list[str]]:
    """
    Task 4: Analyze Alice in Wonderland quote.

    Args:
        string: Optional text to analyze

    Returns:
        tuple: (count_of_all_words, max_len, longest_word_index, odd_words)
    """

    if string is None:
        string = ("So she was considering in her own mind, as well as she could, "
                "for the hot day made her feel very sleepy and stupid, whether "
                "the pleasure of making a daisy-chain would be worth the trouble "
                "of getting up and picking the daisies, when suddenly a White "
                "Rabbit with pink eyes ran close by her.")

    words = [word.strip(strlib.punctuation) for word in string.split()]
    words = [word for word in words if word]
    if not words:
        return 0, 0, 0, []

    # a) word count
    count_words = len(words)

    # b) Longest word and index(0-base)
    longest_word = max(words, key=len)
    max_len = len(longest_word)
    index = next(i for i, word in enumerate(words) if word == longest_word) + 1

    # c) Odd words: 1st, 3rd, 5th... (indices 0, 2, 4...)
    odd_words = [words[i] for i in range(0, len(words), 2)]

    return count_words, max_len, index, odd_words

def task_5(array: list[float]) -> tuple[float, float, int, int]:
    """
    Process list of real numbers.

    Args:
        array: List of float/int numbers

    Returns:
        tuple: (sum_of_negatives, product_between_min_max, min_index, max_index)

    Raises:
        EmptySequenceError: If list is empty
    """

    if len(array) == 0:
        raise EmptySequenceError("List is empty")

    min_val = min(array)
    max_val = max(array)
    min_index = array.index(min_val)
    max_index = array.index(max_val)

    neg_sum = sum(x for x in array if x < 0)

    start = min(min_index, max_index) + 1
    end = max(min_index, max_index)
    product = 1.0
    for value in array[start:end]:
        product *= value

    return neg_sum, product, min_index, max_index
