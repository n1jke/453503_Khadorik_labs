"""matrix package tests"""

from matrix.models import Matrix


def test_matrix():
    seed = 42
    b = 5
    matrix = Matrix(5, 5)
    matrix.generate(seed)

    report = matrix.calc(b)

    assert len(report.superiors) == 16
    assert report.median == report.np_median
