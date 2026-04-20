"""input/output functions"""

from functools import wraps


def valid_input(message: str = "Wrong input value!"):
    """Validate input decorator

    Args:
        message (str, optional): _description_. Defaults to "Wrong input value!".
    """
    def validate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                print(message)
                return wrapper(*args, **kwargs)
        return wrapper
    return validate


@valid_input("Value should be integer!")
def int_input(message: str = "") -> int:
    """Gets integer input"""
    return int(input(message))


@valid_input("Value should be float!")
def float_input(message: str = "") -> float:
    """Gets float input"""
    return float(input(message))


def ints_input(message: str = "", break_value: int = 0):
    """Input integers list via loop"""
    counter = 0
    print(message)
    while True:
        n = int_input(f"{counter + 1}: ")
        yield n
        counter += 1
        if n == break_value:
            break


def ints_gen_input(message: str = "", seq: list[int] = None) -> list[int]:
    """Input integers list via generator"""
    if seq is None:
        seq = []
    try:
        return seq + [int(i) for i in input(message).split()]
    except ValueError:
        print("Values must be integer nums!")
        return ints_gen_input(message, seq)
