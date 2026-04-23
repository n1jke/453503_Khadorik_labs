"""regex test package"""

from plots.models import Calculator


def test_calculator():
    calculator = Calculator()
    x_min = 2
    x_max = 3
    step = 0.1
    eps = 0.1

    calculator.calculate(x_min, x_max, step, eps)
    report = calculator.report

    for i in report.n:
        assert i == 2
    assert len(report.x) == 10
    assert abs(report.res[0] - 1.0833) <= eps
