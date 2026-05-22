"""Model and relation tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from agency.models import (
    Buyer,
    Deal,
    Employee,
    Owner,
    PropertyType,
    RealEstate,
    UserProfile,
)
from agency.tests.conftest import birth_date_years_ago


@pytest.mark.django_db
class TestPropertyType:
    def test_create_and_str(self):
        pt = PropertyType.objects.create(name='Дом', description='Загородный дом')
        assert pt.name == 'Дом'
        assert str(pt) == 'Дом'


@pytest.mark.django_db
class TestOwner:
    def test_phone_valid(self, owner):
        assert owner.phone == '+375 (29) 100-00-01'

    def test_invalid_phone(self):
        owner = Owner(
            full_name='Test',
            phone='80291234567',
            email='a@b.by',
        )
        with pytest.raises(ValidationError):
            owner.full_clean()


@pytest.mark.django_db
class TestRealEstate:
    def test_fk_relations(self, real_estate, property_type, owner):
        assert real_estate.property_type_id == property_type.pk
        assert real_estate.owner_id == owner.pk

    def test_str(self, real_estate):
        assert 'TEST-001' in str(real_estate)


@pytest.mark.django_db
class TestEmployee:
    def test_one_to_one_user(self, employee_user):
        emp = employee_user.employee_profile
        assert emp.user_id == employee_user.pk
        assert User.objects.filter(employee_profile=emp).exists()


@pytest.mark.django_db
class TestBuyer:
    def test_age_validation_under_18(self):
        buyer = Buyer(
            full_name='Молодой',
            phone='+375 (29) 111-11-11',
            email='y@t.by',
            birth_date=birth_date_years_ago(16),
        )
        with pytest.raises(ValidationError):
            buyer.full_clean()

    def test_age_validation_ok(self, client_user):
        buyer = client_user.buyer_profile
        assert calculate_age_safe(buyer.birth_date) >= 18


def calculate_age_safe(birth_date):
    today = date.today()
    return (
        today.year - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


@pytest.mark.django_db
class TestDeal:
    def test_fk_relations(self, deal, real_estate, employee_user, client_user):
        assert deal.real_estate_id == real_estate.pk
        assert deal.employee_id == employee_user.employee_profile.pk
        assert deal.buyer_id == client_user.buyer_profile.pk

    def test_str(self, deal):
        assert 'TEST-001' in str(deal) or 'Продажа' in str(deal)


@pytest.mark.django_db
class TestOwnerProtect:
    def test_delete_owner_protected(self, owner, real_estate):
        with pytest.raises(ProtectedError):
            owner.delete()


@pytest.mark.django_db
class TestUserProfile:
    def test_default_role_client(self, client_user):
        assert client_user.profile.role == UserProfile.ROLE_CLIENT
