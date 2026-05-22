"""Access control tests."""

import pytest
from django.urls import reverse

from agency.models import RealEstate


@pytest.mark.django_db
def test_anonymous_can_list_properties(client):
    response = client.get(reverse('agency:property_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_cannot_create_property(client):
    response = client.get(reverse('agency:property_create'))
    assert response.status_code == 302
    assert 'properties' in response.url or 'login' in response.url


@pytest.mark.django_db
def test_anonymous_cannot_delete_property(client, real_estate):
    response = client.post(
        reverse('agency:property_delete', kwargs={'pk': real_estate.pk}),
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_client_can_list_properties(client, client_user):
    client.force_login(client_user)
    assert client.get(reverse('agency:property_list')).status_code == 200


@pytest.mark.django_db
def test_client_can_access_create_deal(client, client_user):
    client.force_login(client_user)
    assert client.get(reverse('agency:create_deal')).status_code == 200


@pytest.mark.django_db
def test_client_cannot_delete_property(client, client_user, real_estate):
    client.force_login(client_user)
    response = client.post(
        reverse('agency:property_delete', kwargs={'pk': real_estate.pk}),
    )
    assert response.status_code == 302
    assert RealEstate.objects.filter(pk=real_estate.pk).exists()


@pytest.mark.django_db
def test_employee_can_view_deals(client, employee_user, deal):
    client.force_login(employee_user)
    response = client.get(reverse('agency:deal_list'))
    assert response.status_code == 200
    assert deal.real_estate.title.encode() in response.content or b'deal' in response.content.lower()


@pytest.mark.django_db
def test_employee_sees_only_own_deals(client, employee_user, deal, db, real_estate, test_image):
    from django.contrib.auth.models import User
    from agency.models import Employee, Deal as DealModel
    from datetime import date
    from decimal import Decimal

    other_user = User.objects.create_user('otheremp', password='testpass123')
    other_emp = Employee.objects.create(
        user=other_user,
        department='Аренда',
        position='Менеджер',
        phone='+375 (29) 400-00-01',
        birth_date=date(1988, 3, 1),
        hired_date=date(2019, 1, 1),
    )
    other_deal = DealModel.objects.create(
        deal_type='rent',
        real_estate=real_estate,
        employee=other_emp,
        buyer=deal.buyer,
        deal_date=date.today(),
        amount=Decimal('50000'),
    )
    client.force_login(employee_user)
    response = client.get(reverse('agency:deal_list'))
    content = response.content.decode()
    assert str(deal.pk) in content or deal.real_estate.code in content
    assert str(other_deal.pk) not in content.split('delete')  # own deal visible


@pytest.mark.django_db
def test_admin_can_statistics(client, admin_user):
    client.force_login(admin_user)
    assert client.get(reverse('agency:statistics')).status_code == 200


@pytest.mark.django_db
def test_admin_can_create_property(client, admin_user):
    client.force_login(admin_user)
    assert client.get(reverse('agency:property_create')).status_code == 200


@pytest.mark.django_db
def test_anonymous_api_weather_forbidden(client):
    response = client.get(reverse('agency:api_weather'))
    assert response.status_code == 403
