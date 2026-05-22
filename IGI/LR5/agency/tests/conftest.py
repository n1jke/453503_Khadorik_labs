"""Shared pytest-django fixtures."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from agency.models import (
    Buyer,
    Deal,
    Employee,
    Owner,
    PropertyType,
    RealEstate,
    UserProfile,
)

def _make_png_bytes():
    from io import BytesIO
    from PIL import Image
    buffer = BytesIO()
    Image.new('RGB', (10, 10), color=(100, 120, 140)).save(buffer, format='PNG')
    return buffer.getvalue()


@pytest.fixture
def test_image():
    return SimpleUploadedFile(
        'test.png',
        _make_png_bytes(),
        content_type='image/png',
    )


@pytest.fixture
def property_type(db):
    return PropertyType.objects.create(
        name='Квартира',
        description='Жилое помещение',
    )


@pytest.fixture
def owner(db):
    return Owner.objects.create(
        full_name='Иванов Иван',
        phone='+375 (29) 100-00-01',
        email='owner@test.by',
    )


@pytest.fixture
def real_estate(db, property_type, owner, test_image):
    return RealEstate.objects.create(
        code='TEST-001',
        title='Тестовая квартира',
        address='г. Минск, ул. Тест, 1',
        area=Decimal('50.00'),
        price=Decimal('100000.00'),
        rooms=2,
        floor=5,
        description='Описание тестового объекта',
        photo=test_image,
        property_type=property_type,
        owner=owner,
        status=RealEstate.STATUS_AVAILABLE,
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='testadmin',
        email='admin@test.by',
        password='testpass123',
    )


@pytest.fixture
def employee_user(db):
    user = User.objects.create_user(
        username='testemployee',
        password='testpass123',
        email='emp@test.by',
    )
    Employee.objects.create(
        user=user,
        department='Продажи',
        position='Риелтор',
        phone='+375 (29) 200-00-01',
        birth_date=date(1990, 1, 15),
        hired_date=date(2020, 6, 1),
    )
    UserProfile.objects.filter(user=user).update(role=UserProfile.ROLE_EMPLOYEE)
    return user


@pytest.fixture
def client_user(db):
    user = User.objects.create_user(
        username='testclient',
        password='testpass123',
        email='client@test.by',
    )
    UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': UserProfile.ROLE_CLIENT},
    )
    Buyer.objects.create(
        user=user,
        full_name='Клиент Тест',
        phone='+375 (29) 300-00-01',
        email='client@test.by',
        birth_date=date(1995, 5, 20),
    )
    return user


@pytest.fixture
def deal(db, real_estate, employee_user, client_user):
    buyer = client_user.buyer_profile
    employee = employee_user.employee_profile
    return Deal.objects.create(
        deal_type=Deal.DEAL_SALE,
        real_estate=real_estate,
        employee=employee,
        buyer=buyer,
        deal_date=date.today(),
        amount=Decimal('95000.00'),
    )


def birth_date_years_ago(years):
    """Birth date exactly N years ago (same month/day)."""
    today = date.today()
    try:
        return date(today.year - years, today.month, today.day)
    except ValueError:
        return date(today.year - years, today.month, 28)
