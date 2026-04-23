"""tests for forest package"""

from serialize.models import Forest, Tree


def test_add_trees():
    forest = Forest()

    forest.add_trees(Tree("name", 42, 42))
    forest.add_trees(Tree("name", 42, 42))

    assert len(forest.trees) == 2


def test_sort_trees():
    forest = Forest()
    forest.add_trees(Tree("name", 3, 42))
    forest.add_trees(Tree("name", 1, 42))
    forest.add_trees(Tree("name", 2, 42))

    forest.sort()

    assert forest.trees[0].count == 1
    assert forest.trees[1].count == 2
    assert forest.trees[2].count == 3


def test_trees_count():
    forest = Forest()
    forest.add_trees(Tree("name", 5, 4))
    forest.add_trees(Tree("name", 4, 2))
    forest.add_trees(Tree("name", 3, 1))

    assert forest.get_trees_count() == 12


def test_health_trees_count():
    forest = Forest()
    forest.add_trees(Tree("name", 5, 4))
    forest.add_trees(Tree("name", 4, 2))
    forest.add_trees(Tree("name", 3, 1))

    assert forest.get_trees_health_count() == 7


def test_trees_seek_percent():
    forest = Forest()
    forest.add_trees(Tree("name", 5, 4))
    forest.add_trees(Tree("name", 4, 2))
    forest.add_trees(Tree("name", 3, 1))

    assert forest.get_sick_percent() == (1 - 7 / 12) * 100


def test_trees_percents():
    forest = Forest()
    forest.add_trees(Tree("name1", 5, 4))
    forest.add_trees(Tree("name1", 5, 4))
    forest.add_trees(Tree("name2", 5, 4))
    forest.add_trees(Tree("name2", 4, 2))
    forest.add_trees(Tree("name2", 3, 1))

    percents = forest.get_trees_percents()

    eps = 0.01
    assert abs(percents['name1'] - 10 / 22 * 100) < eps
    assert abs(percents['name2'] - 12 / 22 * 100) < eps
    assert abs(percents['name1 sick'] - 2 / 22 * 100) < eps
    assert abs(percents['name2 sick'] - 5 / 22 * 100) < eps
