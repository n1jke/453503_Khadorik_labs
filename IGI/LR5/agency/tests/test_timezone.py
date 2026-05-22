"""Timezone and date format tests."""

import pytest
from django.test import RequestFactory

from agency.timezone_utils import (
    format_date_ddmmyyyy,
    get_datetime_context,
    get_user_timezone,
    is_valid_timezone,
)


def test_is_valid_timezone():
    assert is_valid_timezone('Europe/Minsk')
    assert not is_valid_timezone('Invalid/Zone')


@pytest.mark.django_db
def test_get_user_timezone_default():
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    request.user = type('U', (), {'is_authenticated': False})()
    tz = get_user_timezone(request)
    assert str(tz) == 'Europe/Minsk'


@pytest.mark.django_db
def test_datetime_context_format(client_user):
    factory = RequestFactory()
    request = factory.get('/')
    request.session = {}
    request.user = client_user
    ctx = get_datetime_context(request)
    assert '/' in ctx['current_date_utc']
    assert len(ctx['current_date_utc'].split('/')) == 3
    assert 'text_calendar' in ctx
    assert len(ctx['text_calendar']) > 10


def test_format_date_ddmmyyyy():
    from datetime import datetime
    from django.utils import timezone as dj_tz
    dt = dj_tz.make_aware(datetime(2024, 3, 15, 12, 0))
    assert format_date_ddmmyyyy(dt) == '15/03/2024'
