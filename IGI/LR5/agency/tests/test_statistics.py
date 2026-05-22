"""Statistics calculation tests."""

from datetime import date
from decimal import Decimal

import pytest
from django.db.models import Sum

from agency.models import Buyer, Deal, PropertyType, RealEstate
from agency.statistics_calc import compute_statistics
from agency.tests.conftest import birth_date_years_ago


@pytest.mark.django_db
def test_total_deals_sum(deal):
    stats = compute_statistics()
    expected = float(
        Deal.objects.aggregate(s=Sum('amount'))['s'] or 0,
    )
    assert stats['total_deals_sum'] == expected


@pytest.mark.django_db
def test_deal_mean_median(deal, db, real_estate, employee_user, client_user):
    Deal.objects.create(
        deal_type=Deal.DEAL_RENT,
        real_estate=real_estate,
        employee=employee_user.employee_profile,
        buyer=client_user.buyer_profile,
        deal_date=date.today(),
        amount=Decimal('105000.00'),
    )
    stats = compute_statistics()
    assert stats['deal_stats']['count'] >= 2
    assert stats['deal_stats']['mean'] > 0
    assert stats['deal_stats']['median'] > 0


@pytest.mark.django_db
def test_client_age_stats(client_user):
    stats = compute_statistics()
    assert stats['age_stats']['count'] >= 1
    assert stats['age_stats']['mean'] >= 18
    assert stats['age_stats']['median'] >= 18


@pytest.mark.django_db
def test_popular_and_profitable_type(deal, property_type):
    stats = compute_statistics()
    assert stats['popular_type'] is not None
    assert stats['profitable_type'] is not None
    assert stats['popular_type'].deal_count >= 1


@pytest.mark.django_db
def test_employee_stats(deal, employee_user):
    stats = compute_statistics()
    assert len(stats['employees_stats']) >= 1
    emp_stat = stats['employees_stats'][0]
    assert emp_stat.deal_count >= 1
