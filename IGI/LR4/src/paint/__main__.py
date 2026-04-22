"""shape task package"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from paint.utils import input_rhomb, plot


def main():
    rhombus = None

    while True:
        cmd = input("$ ").strip()
        match cmd:
            case "rhomb":
                rhombus = input_rhombus()
                if rhombus is None:
                    continue
                print(
                    f"Rhombus:\n{rhombus:name side_size angle color area}", end="")
            case "info":
                if rhombus is None:
                    print("Shape is none!")
                    continue
                print(f"{rhombus: name side_size angle color area}", end="")
            case "plot":
                if rhombus is not None:
                    plot(rhombus)
            case "help":
                commands = ["rhomb", "info", "plot", "help", "quit"]
                for c in commands:
                    print(f"   {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
