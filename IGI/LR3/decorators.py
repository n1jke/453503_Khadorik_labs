"""
Decorators for function enhancement.
Lab: 3, Variant: 26
Developer: Matvey Khadorik
Date: 2026-03-20
Version: 1.0
"""

import functools
import time
from typing import Callable, Any


def timer_decorator(func: Callable) -> Callable:
    """
    Decorator to measure execution time.
    Usage: @timer_decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"[TIMER] {func.__name__} executed in {elapsed:.6f} seconds")
        return result
    return wrapper


def log_calls(func: Callable) -> Callable:
    """
    Decorator to log function calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"[LOG] Calling {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"[LOG] {func.__name__} returned {result!r}")
            return result
        except Exception as e:
            print(f"[LOG] {func.__name__} raised {e.__class__.__name__}: {e}")
            raise
    return wrapper


def validate_positive(func: Callable) -> Callable:
    """Validate that first argument is positive."""
    @functools.wraps(func)
    def wrapper(x, *args, **kwargs):
        if x <= 0:
            raise ValueError(f"First argument must be positive, got {x}")
        return func(x, *args, **kwargs)
    return wrapper
