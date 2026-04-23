"""planets task package"""

import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from planets.models import PlanetsDfProcessor


def main():
    """main hosts module terminal"""
    df = None

    while True:
        cmd = input("$ ").strip()
        match cmd:
            case "read":
                df = pd.read_csv(input("Dataset csv path: "))
            case "info":
                if df is None:
                    print("Dataframe is None!")
                    continue
                print(PlanetsDfProcessor.filter_by_mass(df))
                print(f"Max/min period: {PlanetsDfProcessor.period_ratio(df)}")
            case "help":
                commands = ["read", "info", "help", "quit"]
                for c in commands:
                    print(f"  {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
