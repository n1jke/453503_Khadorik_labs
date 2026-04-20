"""models module"""

from dataclasses import dataclass, asdict


class ToStringMixin:
    def __str__(self):
        return str(asdict(self))


@dataclass
class Tree(ToStringMixin):
    """Info about trees of some type"""
    name: str
    count: int
    health_count: int


class Forest:
    def __init__(self):
        self._trees: list[Tree] = []

    def add_trees(self, value: Tree) -> None:
        """add trees in trees list"""
        self._trees.append(value)

    def get_trees(self) -> list[Tree]:
        """trees list setter"""
        return self._trees

    def set_trees(self, value) -> None:
        self._trees = value

    trees = property(get_trees, set_trees)

    def sort(self) -> None:
        """sort trees list"""
        self._trees.sort(key=lambda t: t.count)

    def get_trees_count(self) -> int:
        """common trees count in forest"""
        count = 0
        for t in self.trees:
            count += t.count
        return count

    def get_trees_health_count(self) -> int:
        """common trees health count in forest"""
        count = 0
        for t in self.trees:
            count += t.health_count
        return count

    def get_sick_percent(self) -> float:
        """sick tress percentage"""
        return (1 - self.get_trees_health_count() / self.get_trees_count()) * 100

    def get_trees_percents(self) -> dict[str, float]:
        """all trees types percents"""
        counts = {}
        for t in self._trees:
            if t.name in counts:
                counts[t.name] += t.count
                counts[f"{t.name} sick"] += t.count - t.health_count
            else:
                counts[t.name] = t.count
                counts[f"{t.name} sick"] = t.count - t.health_count

        count = self.get_trees_count()
        result = {}
        for k, v in counts.items():
            result[k] = v / count * 100
        return result
