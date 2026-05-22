"""View and logging tests."""

import logging

import pytest
from django.urls import reverse

from agency.tests.conftest import birth_date_years_ago


@pytest.mark.django_db
def test_home_view(client):
    assert client.get(reverse('agency:home')).status_code == 200


@pytest.mark.django_db
def test_login_success(client, client_user):
    response = client.post(reverse('agency:login'), {
        'username': 'testclient',
        'password': 'testpass123',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_failure(client):
    response = client.post(reverse('agency:login'), {
        'username': 'nobody',
        'password': 'wrong',
    })
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(client, client_user):
    client.force_login(client_user)
    assert client.get(reverse('agency:logout')).status_code == 302


@pytest.mark.django_db
def test_register_view(client):
    response = client.post(reverse('agency:register'), {
        'username': 'brandnew',
        'email': 'brand@test.by',
        'password': 'securepass123',
        'password_confirm': 'securepass123',
        'full_name': 'Новый Клиент',
        'phone': '+375 (29) 777-88-99',
        'birth_date': birth_date_years_ago(25),
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_about_glossary_contacts(client):
    assert client.get(reverse('agency:about')).status_code == 200
    assert client.get(reverse('agency:glossary')).status_code == 200
    assert client.get(reverse('agency:contacts')).status_code == 200


@pytest.mark.django_db
def test_promocodes_vacancies_privacy(client):
    assert client.get(reverse('agency:promocodes')).status_code == 200
    assert client.get(reverse('agency:vacancies')).status_code == 200
    assert client.get(reverse('agency:privacy')).status_code == 200


@pytest.mark.django_db
def test_statistics_redirect_anonymous(client):
    response = client.get(reverse('agency:statistics'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_deal_post(client, client_user, real_estate, employee_user):
    client.force_login(client_user)
    response = client.post(reverse('agency:create_deal'), {
        'real_estate': real_estate.pk,
        'deal_type': 'sale',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_logging_on_login(client, client_user, caplog):
    with caplog.at_level(logging.INFO, logger='agency'):
        client.post(reverse('agency:login'), {
            'username': 'testclient',
            'password': 'testpass123',
        })
    assert any('logged in' in r.message for r in caplog.records)
