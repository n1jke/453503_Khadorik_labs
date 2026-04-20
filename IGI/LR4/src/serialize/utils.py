"""01_serialize package utils"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared import io
from serializers import CsvSerializer, PickleSerializer
from models import Forest, Tree


def input_trees() -> Tree:
    """input trees from user"""
    name = input("Tree name: ")
    count = io.int_input("Count: ")
    health_count = io.int_input("Health count: ")
    return Tree(name, count, health_count)


def write(forest: Forest) -> None:
    """write func"""
    serializer_str = input("Format (csv, pickle): ").strip()
    filename = input("Filename: ").strip()
    serializer = None
    match serializer_str:
        case CsvSerializer.file_type:
            serializer = CsvSerializer()
        case PickleSerializer.file_type:
            serializer = PickleSerializer()
        case _:
            print("Wrong format!")
            return
    serializer.write(filename, forest.trees)


def read() -> Forest:
    """read func"""
    filename = input("Filename: ").strip()
    serializer = None
    match filename.rsplit(".", maxsplit=1)[-1]:
        case CsvSerializer.file_type:
            serializer = CsvSerializer()
        case PickleSerializer.file_type:
            serializer = PickleSerializer()
        case _:
            return None
    forest = Forest()
    forest.trees = serializer.read(filename, Tree)
    return forest


def info(forest: Forest) -> None:
    """info about forest"""
    print(f"    Count: {forest.get_trees_count()}")
    print(f"    Health count: {forest.get_trees_health_count()}")
    print(f"    Sick percent: {forest.get_sick_percent():.2f}")
    print("    Trees count: ")
    for k, v in forest.get_trees_percents().items():
        print(f"      {k}: {v:.2f}")
