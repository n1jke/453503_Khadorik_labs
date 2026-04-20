"""regex task package"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from regex.models import Analizer
from regex.utils import read, write


def main():
    """main hosts module terminal"""
    analizer = Analizer()

    while True:
        cmd = input("$ ").strip()
        match cmd:
            case "read":
                analizer.text = read()
            case "analize":
                analizer.analize()
                print(analizer.report)
            case "info":
                print(f"Text: \n{analizer.text}")
                if analizer.report is not None:
                    print(analizer.report)
            case "clear":
                analizer.text = ""
            case "write":
                write(analizer.report)
            case "help":
                commands = ["read", "analize", "info", "clear",
                            "write", "help", "quit"]
                for c in commands:
                    print(f"  {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
