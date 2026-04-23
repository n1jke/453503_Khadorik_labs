"""paint package tests"""

import math
from paint.models import Rhomb


def test_rhomb():
    side_size = 5
    angle = 30
    color = "red"

    rhombus = Rhomb(side_size, math.radians(angle), color)

    assert abs(rhombus.area() - 12.49) < 0.01

    points = rhombus.points()
    expected_points = [[0, 4.829], [1.29, 4.829 * 2],
                       [1.29 * 2, 4.829], [1.29, 0]]

    for a, b in zip(sum(points, []), sum(expected_points, [])):
        assert abs(a - b) < 0.01


def test_format():
    side_size = 5
    angle = 30
    color = "red"

    rhombus = Rhomb(side_size, math.radians(angle), color)
    res = f"{rhombus:rhombus:name side_size angle color area}"

    print(res)

    assert res == "Side: 5\n" \
        "Angle: 30.0\n" \
        "Color: red\n" \
        "Area: 12.499999999999998\n"
