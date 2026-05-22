"""API services and helper module tests."""

from unittest.mock import MagicMock, patch

import pytest

from agency.querysets import filter_properties
from agency.roles import ROLE_ADMIN, ROLE_CLIENT, ROLE_EMPLOYEE, get_user_role
from agency.services import get_exchange_rates, get_weather
from agency.models import RealEstate


@pytest.mark.django_db
def test_get_weather_fallback():
    import requests as req
    with patch('agency.services.requests.get') as mock_get:
        mock_get.side_effect = req.RequestException('network error')
        data = get_weather('Minsk')
    assert 'temperature' in data
    assert data['from_api'] is False


@pytest.mark.django_db
def test_get_weather_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        'name': 'Minsk',
        'main': {'temp': 5.5, 'humidity': 80},
        'weather': [{'description': 'ясно', 'icon': '01d'}],
    }
    mock_resp.raise_for_status = MagicMock()
    from django.conf import settings as django_settings
    with patch('agency.services.requests.get', return_value=mock_resp):
        with patch.object(django_settings, 'OPENWEATHER_API_KEY', 'test-key'):
            data = get_weather('Minsk')
    assert data['from_api'] is True
    assert data['temperature'] == 5.5


@pytest.mark.django_db
def test_get_exchange_rates_fallback():
    import requests as req
    with patch('agency.services.requests.get') as mock_get:
        mock_get.side_effect = req.RequestException('fail')
        data = get_exchange_rates()
    assert 'USD' in data
    assert data['from_api'] is False


@pytest.mark.django_db
def test_filter_properties_search(real_estate):
    qs = RealEstate.objects.all()
    filtered, ctx = filter_properties(qs, {'q': 'Тестовая'})
    assert filtered.filter(pk=real_estate.pk).exists()
    assert ctx['q'] == 'Тестовая'


@pytest.mark.django_db
def test_get_user_role(client_user, admin_user, employee_user):
    assert get_user_role(client_user) == ROLE_CLIENT
    assert get_user_role(admin_user) == ROLE_ADMIN
    assert get_user_role(employee_user) == ROLE_EMPLOYEE
