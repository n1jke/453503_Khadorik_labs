"""
Custom exceptions for Lr-3.
Lr-3, var: 26
Developer: Matvey Khadorik
Date: 2026-03-20
Version: 1.0
"""

class LabException(Exception):
    """Base exception for all lab tasks."""
    pass

class ConvergenceError(LabException):
    """Raised when series does not converge within max iterations."""
    pass

class InvalidDomainError(LabException):
    """Raised when argument is outside valid domain."""
    pass

class EmptySequenceError(LabException):
    """Raised when sequence is empty but must contain elements."""
    pass

class InputValidationError(LabException):
    """Raised when user input validation fails."""
    pass
