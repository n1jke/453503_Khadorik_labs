"""
Sequence initializers using generators (yield).
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Version: 1.0
"""

import random
from typing import List, Generator


def random_float_generator(count: int, min_val: float = -100.0, max_val: float = 100.0) -> Generator[float, None, None]:
    """
    Generator that yields 'count' random float numbers.
    This demonstrates lazy evaluation with yield.

    Args:
        count: Number of values to generate
        min_val: Minimum value
        max_val: Maximum value

    Yields:
        float: Random number in range [min_val, max_val]
    """
    for _ in range(count):
        yield random.uniform(min_val, max_val)


def init_with_generator(sequence: List[float], size: int, min_val: float = -100.0, max_val: float = 100.0) -> List[
    float]:
    """
    Initialize sequence using generator function with yield.

    Args:
        sequence: List to fill (cleared first)
        size: Number of elements
        min_val: Minimum random value
        max_val: Maximum random value

    Returns:
        Modified sequence filled with generated values
    """
    sequence.clear()
    # Используем yield генератор
    gen = random_float_generator(size, min_val, max_val)
    sequence.extend(gen)
    return sequence


def integer_generator(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """
    Infinite generator for sequential integers (like range but lazy).
    Can be used for auto-increment IDs.
    """
    current = start
    while True:
        yield current
        current += step


def cyclic_generator(values: List, repeat: int = 1) -> Generator:
    """
    Generator that cycles through values 'repeat' times.
    """
    for _ in range(repeat):
        for val in values:
            yield val