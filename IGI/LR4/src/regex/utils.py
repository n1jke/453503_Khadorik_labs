"""utils"""

import zipfile
from .models import Report


def read() -> str:
    """read text from file command"""
    file_path = input("File path: ")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return "".join(file.readlines())
    except FileNotFoundError:
        print("File not found!")


def write(report: Report) -> None:
    """write report to txt and zip file"""
    filename = input("File name: ")
    with open(f"{filename}.txt", "w", encoding="utf-8") as file:
        file.write(str(report))
    with zipfile.ZipFile(f"{filename}.zip", "w") as file:
        file.write(f"{filename}.txt")
