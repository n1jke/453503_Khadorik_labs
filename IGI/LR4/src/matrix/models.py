"""models"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Report:
    superiors: np.ndarray
    np_median: float
    median: float

    def __str__(self) -> str:
        return f"Superiors count: {len(self.superiors)}\n" \
            f"Superiors: {self.superiors}\n" \
            f"Numpy median: {self.np_median}\n" \
            f"Default median: {self.median}"


class Matrix:
    def __init__(self, n: int, m: int):
        self._n = n
        self._m = m
        self.generate()

    def generate(self, seed: int | None = None) -> None:
        self._matrix = np.random.default_rng(seed).random((self._n, self._m)) * 10

    @staticmethod
    def median(array: np.ndarray):
        sorted_array = np.sort(array)
        n = len(sorted_array)
        if n % 2 == 1:
            return sorted_array[n // 2]
        return (sorted_array[n // 2 - 1] + sorted_array[n // 2]) / 2

    def calc(self, b: float) -> Report:
        """all matrix elements where abs value > b"""
        superiors = self._matrix[abs(self._matrix) > b]
        return Report(superiors, np.median(superiors), Matrix.median(superiors))

    def __str__(self) -> str:
        return str(self._matrix)
