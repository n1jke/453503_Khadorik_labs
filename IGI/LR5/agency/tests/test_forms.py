"""Form tests."""

from datetime import date

import pytest

from agency.forms import DealForm, RegistrationForm, ReviewForm
from agency.models import RealEstate
from agency.tests.conftest import birth_date_years_ago


@pytest.mark.django_db
def test_registration_form_valid():
    form = RegistrationForm(data={
        'username': 'newuser1',
        'email': 'new@test.by',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
        'full_name': 'Новый Пользователь',
        'phone': '+375 (29) 555-66-77',
        'birth_date': birth_date_years_ago(25),
    })
    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize('missing_field', [
    'username', 'email', 'password', 'full_name', 'phone', 'birth_date',
])
def test_registration_form_empty_field(missing_field):
    data = {
        'username': 'u2',
        'email': 'e@test.by',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
        'full_name': 'Имя',
        'phone': '+375 (29) 555-66-77',
        'birth_date': birth_date_years_ago(25),
    }
    data[missing_field] = ''
    form = RegistrationForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_registration_form_bad_phone():
    form = RegistrationForm(data={
        'username': 'u3',
        'email': 'e3@test.by',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
        'full_name': 'Имя',
        'phone': '80291111111',
        'birth_date': birth_date_years_ago(25),
    })
    assert not form.is_valid()
    assert 'phone' in form.errors


@pytest.mark.django_db
def test_registration_form_under_18():
    form = RegistrationForm(data={
        'username': 'u4',
        'email': 'e4@test.by',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
        'full_name': 'Имя',
        'phone': '+375 (29) 555-66-77',
        'birth_date': birth_date_years_ago(15),
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_deal_form_valid(real_estate):
    form = DealForm(data={
        'real_estate': real_estate.pk,
        'deal_type': 'sale',
    })
    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize('rating, valid', [(1, True), (5, True), (3, True)])
def test_review_form_rating_valid(rating, valid):
    form = ReviewForm(data={
        'rating': rating,
        'text': 'Отличная работа агентства, рекомендую всем!',
    })
    assert form.is_valid() == valid


@pytest.mark.django_db
def test_review_form_short_text():
    form = ReviewForm(data={'rating': 5, 'text': 'Коротко'})
    assert not form.is_valid()
