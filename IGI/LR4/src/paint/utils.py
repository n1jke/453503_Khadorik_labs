"""utils"""

import math
import matplotlib.pyplot as plt
from shared.io import float_input
from .models import Shape, Rhomb


def input_rhomb() -> Rhomb | None:
    """rhomb input"""
    name = input("Name: ")
    side_size = float_input("Side size: ")
    if side_size <= 0:
        print("Value should be positive!")
        return None
    angle = float_input("Angle (degrees): ")
    color = input("Color: ")
    rhomb = Rhomb(side_size, math.radians(angle), color)
    rhomb.name = name
    return rhomb


def plot(shape: Shape) -> None:
    """plot figure"""
    plt.title(shape.name)
    plt.axis('equal')
    plt.fill(*[list(row)
             for row in zip(*shape.points())], color=shape.color.color)
    plt.savefig("shape.png")
    plt.show()
