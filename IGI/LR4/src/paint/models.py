"""models"""

from abc import ABC, abstractmethod
import math


class Color():
    def __init__(self, color: str):
        self._color = color

    @property
    def color(self) -> str:
        """color getter"""
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value

    def __str__(self):
        return self._color


class Shape(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> Color:      
        pass

    @abstractmethod
    def area(self) -> float:    
        pass

    @abstractmethod
    def points(self) -> list[list[float]]:
        pass


class Rhomb(Shape):
    def __init__(self, side_size: float, angle: float, color: str):
        super().__init__()
        self._side_size = side_size
        self._angle = angle
        self._color = Color(color)

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @name.setter
    def name(self, value: str):
        self._name = value

    def area(self) -> float:
        return math.pow(self._side_size, 2) * math.sin(self._angle)

    def points(self) -> list[list[float]]:
        x_h = self._side_size * math.sin(self._angle / 2)
        y_h = self._side_size * math.cos(self._angle / 2)
        return [[0, y_h], [x_h, y_h * 2], [x_h * 2, y_h], [x_h, 0]]

    def __format__(self, format_spec: str):
        frmt = ""
        for param in format_spec.split():
            match param:
                case "name":
                    frmt += f"Name: {self._name}\n"
                case "side_size" | "side":
                    frmt += f"Side: {self._side_size}\n"
                case "color":
                    frmt += f"Color: {self._color}\n"
                case "area":
                    frmt += f"Area: {self.area()}\n"
                case "angle":
                    frmt += f"Angle: {math.degrees(self._angle):.5}\n"
        return frmt
