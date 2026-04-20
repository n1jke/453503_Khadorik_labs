"""write & read with serializers"""

import csv
import pickle
from dataclasses import fields, asdict
from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def write(self, filename: str, data):
        """write to file"""

    @abstractmethod
    def read(self, filename: str, clazz=None):
        """read from file"""


class CsvSerializer(Serializer):
    file_type: str = "csv"

    def write(self, filename: str, data):
        with open(f"{filename}", "w", encoding="utf-8") as file:
            if len(data) > 0:
                writer = csv.DictWriter(file, fieldnames=[f.name for f in fields(data[0])])
                writer.writeheader()
                writer.writerows([asdict(i) for i in data])

    def read(self, filename, clazz=None):
        with open(filename, "r", encoding="utf-8") as file:
            return [clazz(**row) for row in csv.DictReader(file)]


class PickleSerializer(Serializer):
    file_type: str = "pickle"

    def write(self, filename: str, data):
        with open(f"{filename}", "wb") as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def read(self, filename, clazz=None):
        with open(filename, "rb") as file:
            return pickle.load(file)
