"""Кастомные валидаторы для моделей и форм."""

import re
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

PHONE_REGEX_PATTERN = r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$'

PHONE_VALIDATOR = RegexValidator(
    regex=PHONE_REGEX_PATTERN,
    message='Телефон должен быть в формате +375 (29) XXX-XX-XX.',
)

PHONE_INPUT_PATTERN = r'\+375 \(29\) \d{3}-\d{2}-\d{2}'


def validate_phone(value):
    """Проверка телефона по regex (+375 (29) XXX-XX-XX)."""
    if not re.match(PHONE_REGEX_PATTERN, value or ''):
        raise ValidationError(
            'Телефон должен быть в формате +375 (29) XXX-XX-XX.',
            code='invalid_phone',
        )


def calculate_age(birth_date, today=None):
    """Возраст в полных годах по дате рождения."""
    today = today or date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def calculate_age_days(birth_date, today=None):
    """Возраст в годах через целочисленное деление дней (для форм)."""
    today = today or date.today()
    return (today - birth_date).days // 365


def validate_age_18_plus(value):
    """Проверка возраста не менее 18 лет (для моделей)."""
    if calculate_age(value) < 18:
        raise ValidationError(
            'Возраст должен быть не менее 18 лет.',
            code='age_under_18',
        )


def validate_age_18_plus_form(birth_date):
    """Проверка 18+ для форм (расчёт через days // 365)."""
    if calculate_age_days(birth_date) < 18:
        raise ValidationError(
            'Возраст должен быть не менее 18 лет.',
            code='age_under_18',
        )


def validate_non_whitespace(value):
    """Поле не должно состоять только из пробелов."""
    if value is None:
        return
    if not str(value).strip():
        raise ValidationError(
            'Поле не может быть пустым или содержать только пробелы.',
            code='blank_whitespace',
        )


def validate_positive_decimal(value):
    """Число должно быть строго больше нуля."""
    if value is None:
        return
    if Decimal(value) <= 0:
        raise ValidationError(
            'Значение должно быть больше нуля.',
            code='not_positive',
        )
