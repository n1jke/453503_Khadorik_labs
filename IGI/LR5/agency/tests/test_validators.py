"""Custom validator tests."""

from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from agency.validators import (
    calculate_age,
    validate_age_18_plus,
    validate_non_whitespace,
    validate_phone,
    validate_positive_decimal,
)
from agency.tests.conftest import birth_date_years_ago


@pytest.mark.parametrize('phone, expected_valid', [
    ('+375 (29) 123-45-67', True),
    ('+375291234567', False),
    ('80291234567', False),
    ('+375 (33) 123-45-67', False),
    ('', False),
    ('   ', False),
])
def test_phone_validation(phone, expected_valid):
    if expected_valid:
        validate_phone(phone)
    else:
        with pytest.raises(ValidationError):
            validate_phone(phone)


@pytest.mark.parametrize('years_ago, expected_valid', [
    (20, True),
    (18, True),
    (17, False),
    (10, False),
])
def test_age_validation_years_ago(years_ago, expected_valid):
    birth = birth_date_years_ago(years_ago)
    if expected_valid:
        validate_age_18_plus(birth)
    else:
        with pytest.raises(ValidationError):
            validate_age_18_plus(birth)


def test_age_17_years_11_months_fails():
    """17 years and 11 months is under 18."""
    today = date.today()
    birth = today - timedelta(days=17 * 365 + 30)
    assert calculate_age(birth) < 18
    with pytest.raises(ValidationError):
        validate_age_18_plus(birth)


def test_age_future_date_fails():
    future = date.today() + timedelta(days=30)
    with pytest.raises(ValidationError):
        validate_age_18_plus(future)


@pytest.mark.parametrize('value, ok', [
    ('text', True),
    ('  text  ', True),
    ('', False),
    ('   ', False),
])
def test_non_whitespace(value, ok):
    if ok:
        validate_non_whitespace(value)
    else:
        with pytest.raises(ValidationError):
            validate_non_whitespace(value)


@pytest.mark.parametrize('amount, ok', [
    ('100.50', True),
    ('0', False),
    ('-1', False),
])
def test_positive_decimal(amount, ok):
    if ok:
        validate_positive_decimal(amount)
    else:
        with pytest.raises(ValidationError):
            validate_positive_decimal(amount)
