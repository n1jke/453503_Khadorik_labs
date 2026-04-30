"""matrix task package"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared import io
from matrix.models import Matrix


def main():
    """main hosts module terminal"""
    matrix = None

    while True:
        cmd = input("$ ").strip()
        match cmd:
            case "create":
                matrix = Matrix(io.int_input("N: "), io.int_input("M: "))
                print(matrix)
            case "calc":
                if matrix is None:
                    print("Matrix not created")
                    continue
                print(matrix.calc(io.float_input("Value: ")))
            case "gen":
                if matrix is None:
                    print("Matrix is None!")
                    continue
                matrix.generate()
                print(matrix)
            case "help":
                commands = ["create", "calc", "regen", "help", "quit"]
                for c in commands:
                    print(f"  {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
