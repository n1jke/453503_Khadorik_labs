"""
Main entry point for Lab 3.
Combines all modules, handles exceptions, provides repeat capability.
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Version: 1.0
"""

from core import task_1, task_2, task_3, task_4, task_5
from decorators import timer_decorator, log_calls
from exceptions import (
    InvalidDomainError, ConvergenceError, EmptySequenceError
)
from generators import init_with_generator
from io_utils import (
    get_float, get_int, get_string, get_list_interactive,
    get_even_numbers_loop, print_task1_result, print_task2_result,
    print_task4_result, ask_repeat, ask_choice
)


def run_task_1():
    """Run Task 1 with exception handling."""
    try:
        x = get_float("Enter x (|x| > 1): ", min_val=1.000001)
        eps = get_float("Enter eps (e.g., 0.0001): ", min_val=1e-15, max_val=1.0)

        @timer_decorator
        def calculate():
            return task_1(x, eps)

        n, math_val, series_val = calculate()
        print_task1_result(x, n, series_val, math_val, eps)

    except InvalidDomainError as e:
        print(f"[Domain Error] {e}")
    except ConvergenceError as e:
        print(f"[Convergence Error] {e}")
    except Exception as e:
        print(f"[Unexpected Error] {type(e).__name__}: {e}")


def run_task_2():
    """Run Task 2."""
    try:
        numbers = get_even_numbers_loop()
        avg, count, evens = task_2(numbers)
        print_task2_result(avg, count, evens)
    except EmptySequenceError as e:
        print(f"[Error] {e}")


def run_task_3():
    """Run Task 3."""
    text = get_string("Enter text: ")
    count = task_3(text)
    print(f"Words starting with lowercase: {count}")


def run_task_4():
    """Run Task 4."""
    use_default = ask_choice("Use default Alice text? (y/n): ", ['y', 'n']) == 'y'

    text = None if use_default else get_string("Enter your text: ")
    count, max_len, index, odd_words = task_4(text)
    print_task4_result(count, max_len, index, odd_words)


def run_task_5():
    """Run Task 5 with generator initialization option."""
    print("\nInitialization method:")
    print("1. Random generator (yield)")
    print("2. Manual input")

    choice = ask_choice("Select (1/2): ", ['1', '2'])
    lst = []

    try:
        if choice == '1':
            size = get_int("Enter size: ", min_val=1, max_val=1000)
            init_with_generator(lst, size)
            print(f"Generated list: {[f'{x:.2f}' for x in lst]}")
        else:
            lst = get_list_interactive()

        @log_calls
        def process():
            return task_5(lst)

        neg_sum, product, min_i, max_i = process()
        print(f"\nSum of negatives: {neg_sum:.2f}")
        print(f"Min index: {min_i}, Max index: {max_i}")
        print(f"Product between them: {product:.4f}")

    except EmptySequenceError as e:
        print(f"[Error] {e}")
    except Exception as e:
        print(f"[Error] {e}")


def main():
    """
    Main menu with repeat capability.
    Requirement 11: ability to repeat without exit.
    """
    tasks = {
        '1': ("Task 1: Series ln((x+1)/(x-1))", run_task_1),
        '2': ("Task 2: Average of even numbers", run_task_2),
        '3': ("Task 3: Count lowercase words", run_task_3),
        '4': ("Task 4: Alice text analysis", run_task_4),
        '5': ("Task 5: List processing", run_task_5),
    }

    print("=" * 60)
    print("LABORATORY WORK 3, VARIANT 26")
    print("=" * 60)

    while True:
        print("\nAvailable tasks:")
        for key, (name, _) in tasks.items():
            print(f"  {key}. {name}")
        print("  0. Exit")
        print("-" * 40)

        choice = ask_choice("Select task: ", ['0', '1', '2', '3', '4', '5'])

        if choice == '0':
            print("Exiting program. Goodbye!")
            break

        task_name, task_func = tasks[choice]
        print(f"\n{'=' * 40}")
        print(f"Running: {task_name}")
        print(f"{'=' * 40}")

        while True:
            try:
                task_func()
            except KeyboardInterrupt:
                print("\n[Info] Interrupted by user")
            except Exception as e:
                print(f"\n[Critical Error] {type(e).__name__}: {e}")

            # Requirement 11: repeat without exiting program
            if not ask_repeat():
                break


if __name__ == "__main__":
    main()