"""Real estate CRUD tests."""

from decimal import Decimal

import pytest
from django.urls import reverse

from agency.models import RealEstate


@pytest.mark.django_db
def test_property_list_read(client, real_estate):
    response = client.get(reverse('agency:property_list'))
    assert response.status_code == 200
    assert real_estate.title.encode() in response.content


@pytest.mark.django_db
def test_property_detail_read(client, real_estate):
    url = reverse('agency:property_detail', kwargs={'pk': real_estate.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert real_estate.code.encode() in response.content


@pytest.mark.django_db
def test_property_create(admin_user, client, property_type, owner, test_image):
    client.force_login(admin_user)
    response = client.post(reverse('agency:property_create'), {
        'code': 'NEW-CRUD-01',
        'title': 'Новый объект',
        'address': 'г. Минск',
        'area': '45.00',
        'price': '80000.00',
        'rooms': 2,
        'floor': 3,
        'description': 'Новое описание',
        'property_type': property_type.pk,
        'owner': owner.pk,
        'status': RealEstate.STATUS_AVAILABLE,
        'photo': test_image,
    })
    assert response.status_code == 302, response.content[:500]
    assert RealEstate.objects.filter(code='NEW-CRUD-01').exists()


@pytest.mark.django_db
def test_property_update(admin_user, client, real_estate, property_type, owner):
    client.force_login(admin_user)
    url = reverse('agency:property_update', kwargs={'pk': real_estate.pk})
    response = client.post(url, {
        'code': real_estate.code,
        'title': 'Обновлённый заголовок',
        'address': real_estate.address,
        'area': str(real_estate.area),
        'price': str(real_estate.price),
        'rooms': real_estate.rooms,
        'floor': real_estate.floor,
        'description': real_estate.description,
        'property_type': property_type.pk,
        'owner': owner.pk,
        'status': real_estate.status,
    })
    assert response.status_code == 302
    real_estate.refresh_from_db()
    assert real_estate.title == 'Обновлённый заголовок'


@pytest.mark.django_db
def test_property_delete(admin_user, client, real_estate):
    pk = real_estate.pk
    client.force_login(admin_user)
    url = reverse('agency:property_delete', kwargs={'pk': pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not RealEstate.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_create_then_in_list(admin_user, client, property_type, owner, test_image):
    client.force_login(admin_user)
    client.post(reverse('agency:property_create'), {
        'code': 'LIST-CRUD-02',
        'title': 'Для списка',
        'address': 'Адрес',
        'area': '30',
        'price': '50000',
        'rooms': 1,
        'floor': 1,
        'description': 'Desc',
        'property_type': property_type.pk,
        'owner': owner.pk,
        'status': 'available',
        'photo': test_image,
    })
    response = client.get(reverse('agency:property_list'))
    assert b'LIST-CRUD-02' in response.content
