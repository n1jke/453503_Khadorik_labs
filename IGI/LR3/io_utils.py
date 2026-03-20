"""
Input/Output operations and validation.
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Version: 1.0
"""

from typing import List, Optional

from exceptions import EmptySequenceError


def get_float(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float | None:
    """
    Get validated float input with protection against invalid data.

    Args:
        prompt: Display prompt
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Validated float value
    """
    while True:
        try:
            value = input(prompt).strip()
            num = float(value)

            if min_val is not None and num < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and num > max_val:
                print(f"Value must be <= {max_val}")
                continue

            return num

        except ValueError:
            print("Invalid number format. Use dot as decimal separator (e.g., 3.14)")


def get_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int | None:
    """
     Get validated int input with protection against invalid data.

     Args:
         prompt: Display prompt
         min_val: Minimum allowed value
         max_val: Maximum allowed value

     Returns:
         Validated int value
     """

    while True:
        try:
            value = input(prompt).strip()
            num = int(value)

            if min_val is not None and num < min_val:
                print(f"[Error] Value must be >= {min_val}")
                continue
            if max_val is not None and num > max_val:
                print(f"[Error] Value must be <= {max_val}")
                continue

            return num
        except ValueError:
            print("[Error] Please enter a valid integer")


def get_string(prompt: str, allow_empty: bool = False) -> str:
    """
       Get validated string input with protection against invalid data.

       Args:
           prompt: Display prompt
           allow_empty: Allow empty string

       Returns:
           Validated string value
       """

    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("[Error] Empty input not allowed")
            continue
        return value


def get_list_interactive() -> List[float]:
    """
    Interactive list input.
    User enters size first, then elements one by one.
    """

    size = get_int("Enter list size: ", min_val=1)
    result = []
    print(f"Enter {size} numbers:")
    for i in range(size):
        num = get_float(f"  Element [{i + 1}/{size}]: ")
        result.append(num)
    return result


def get_even_numbers_loop() -> List[int]:
    """
    Task 2 specific: Read integers until 1 is entered.
    Returns list of all entered numbers (except the terminating 1).
    """

    numbers = []
    print("Enter integers (enter 1 to stop):")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            num = int(user_input)

            if num == 1:
                break
            numbers.append(num)

        except ValueError:
            print("[Error] Please enter a valid integer")
        except KeyboardInterrupt:
            print("\n[Info] Input interrupted")
            break

    if not numbers:
        raise EmptySequenceError("No numbers were entered")

    return numbers


def print_task1_result(x: float, n: int, series_val: float, math_val: float, eps: float):
    """Format Task 1 results as table."""
    print(f"\n{'=' * 70}")
    print(f"{'x':^12} | {'n':^8} | {'F(x) (series)':^15} | {'Math F(x)':^15} | {'eps':^10}")
    print(f"{'-' * 70}")
    print(f"{x:^12.4f} | {n:^8} | {series_val:^15.10f} | {math_val:^15.10f} | {eps:^10.2e}")
    print(f"{'=' * 70}")


def print_task2_result(avg: float, count: int, evens: List[int]):
    """Print Task 2 results."""
    print(f"\nEven numbers found: {evens}")
    print(f"Count: {count}")
    print(f"Average: {avg:.4f}")


def print_task4_result(count: int, max_len: int, index: int, odd_words: str):
    """Print Task 4 results."""
    print(f"\na) Total words: {count}")
    print(f"b) Longest word length: {max_len}, position: {index}")
    print(f"c) Odd words (1st, 3rd, 5th...): {odd_words[:100]}...")


def ask_repeat() -> bool:
    """
    Ask user if they want to repeat the task.
    Requirement 11
    """
    choice = input("\nRepeat this task? (y/n): ").strip().lower()
    return choice == 'y'


def ask_choice(prompt: str, valid_choices: List[str]) -> str:
    """Ask for choice from valid options."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Valid options: {valid_choices}")