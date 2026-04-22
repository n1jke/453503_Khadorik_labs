"""series task package"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared.io import float_input
from plots.models import Calculator


def main():
    """main hosts module terminal"""
    calculator = Calculator()

    while True:
        cmd = input("$ ").strip()
        match cmd:
            case "calc":
                x_min = float_input("Min x: ")
                if x_min <= 1:
                    print("Value should be greater than 1!")
                    continue
                x_max = float_input("Min y: ")
                step = float_input("Step: ")
                eps = float_input("Epsilon: ")
                calculator.calculate(x_min, x_max, step, eps)
                print(calculator.report)
            case "info":
                if calculator.report is not None:
                    print(calculator.report)
            case "plot":
                if calculator.report is not None:
                    calculator.report.plot()
            case "help":
                commands = ["calc", "info", "plot", "help", "quit"]
                for c in commands:
                    print(f"  {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
