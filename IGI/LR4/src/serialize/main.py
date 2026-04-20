"""Main entrypoint for task 01_serialize."""

from utils import Forest, input_trees, write, read, info


def main() -> None:
    """Run interactive forest manager."""
    forest = Forest()

    while True:
        cmd = input("cmd: ").strip()
        match cmd:
            case "trees":
                for t in forest.trees:
                    print(f"    {t}")
            case "add":
                forest.add_trees(input_trees())
            case "sort":
                forest.sort()
            case "info":
                info(forest)
            case "clear":
                forest = Forest()
            case "write":
                write(forest)
            case "read":
                current_forest = read()
                if current_forest is None:
                    print("Something wrong!")
                else:
                    forest = current_forest
            case "help":
                commands = [
                    "trees", "add", "sort", "info",
                    "clear", "write", "read", "help", "quit"
                ]
                for c in commands:
                    print(f"    {c}")
            case "quit":
                return
            case _:
                print("Command not found!")


if __name__ == "__main__":
    main()
