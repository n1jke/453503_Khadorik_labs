"""
Task 1-5:
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Version: 1.0
"""

import math

from exceptions import InvalidDomainError, ConvergenceError, EmptySequenceError

MAX_ITERATIONS_SERIES = 500

def task_1(x : float, eps: float) -> tuple[int, float, float]:
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

    if math.fabs(x) < 1:
        raise InvalidDomainError(f"Domain error: |x| must be > 1, got {x}")

    target = math.log((x + 1) / (x-1))
    series = 0
    n = 0

    while math.fabs(series - target) > eps:
        series += 2 * (1 / ((2*x + 1) * math.pow(x, 2*x + 1)))
        print(series)
        n += 1
        if n > MAX_ITERATIONS_SERIES:
            raise ConvergenceError(f"Series did not converge in {MAX_ITERATIONS_SERIES} iterations")

    return n, target, series


def task_2(array : list[int]) -> float:
    """
    Calculates average of numbers from given list.

    Returns:
        tuple: (average, count_of_all_numbers, list_of_even_numbers)

    Raises:
        EmptySequenceError: If even numbers not found
    """

    even_sum = 0
    even_count = 0

    for item in array:
        if item % 2 == 0:
            even_sum += item
            even_count += 1

    if even_count == 0:
        raise EmptySequenceError("No even numbers found in sequence")
    else:
        return even_sum / even_count

def task_3(string : str) -> int:
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
        clean = word.strip()
        if clean and clean[0].islower():
            n += 1

    return n

def task_4(string : str = None) -> tuple[int,int, int, str]:
    """
    Task 4: Analyze Alice in Wonderland quote.

    Args:
        string: Optional text to analyze

    Returns:
        tuple: (count_of_all_numbers, max_len, longest_word_index, new_string)
    """

    if string is None:
        string = ("So she was considering in her own mind, as well as she could, "
                "for the hot day made her feel very sleepy and stupid, whether "
                "the pleasure of making a daisy-chain would be worth the trouble "
                "of getting up and picking the daisies, when suddenly a White "
                "Rabbit with pink eyes ran close by her.")

    words = string.split()

    # a) word count
    count_words = len(words)

    # b) Longest word and index(0-base)
    longest_length = -1
    longest_index = -1
    for i, word in enumerate(words):
        if len(words[i]) > longest_length:
            max_len = len(words[i])
            index = i

    # c) Odd words: 1st, 3rd, 5th... (indices 0, 2, 4...)
    odd_words = [words[i] for i in range(0, len(words), 2)]
    new_string = ""
    for word in words:
        if word[0] != "a":
            new_string += " " + word


    return count_words,longest_length,longest_index, new_string

def task_5(array : list[int]) -> tuple[int, int]:
    """
    Process list of real numbers.

    Args:
        array: List of float/int numbers

    Returns:
        tuple: (number_sum, number_multiply)

    Raises:
        EmptySequenceError: If list is empty
    """

    if len(array) == 0:
        raise EmptySequenceError("List is empty")

    min_val = min(array)
    max_val = max(array)
    min_index = array.index(min_val)
    max_index = array.index(max_val)

    num_sum = 0
    num_multiply = 1
    for i in range(min_index, max_index):
        if array[i] < 0:
            num_sum += array[i]
            num_multiply *= array[i]


    return num_sum,num_multiply


