"""Таймзоны пользователя, формат DD/MM/YYYY, текстовый календарь."""

import calendar

from django.utils import timezone
from zoneinfo import ZoneInfo, available_timezones

DEFAULT_TZ = 'Europe/Minsk'

COMMON_TIMEZONES = sorted([
    'Europe/Minsk',
    'Europe/Moscow',
    'Europe/Warsaw',
    'Europe/Kiev',
    'UTC',
    'America/New_York',
    'Asia/Dubai',
])


def get_user_timezone(request):
    """
    Определить таймзону через zoneinfo:
    профиль → сессия → заголовок X-Timezone → Europe/Minsk.
    """
    if hasattr(request, 'user') and request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and getattr(profile, 'timezone', None):
            try:
                return ZoneInfo(profile.timezone)
            except (KeyError, ValueError):
                pass

    session_tz = request.session.get('user_timezone')
    if session_tz:
        try:
            return ZoneInfo(session_tz)
        except (KeyError, ValueError):
            pass

    tz_header = request.headers.get('X-Timezone') or request.META.get(
        'HTTP_X_TIMEZONE',
    )
    if tz_header:
        try:
            return ZoneInfo(tz_header)
        except (KeyError, ValueError):
            pass

    return ZoneInfo(DEFAULT_TZ)


def format_datetime_ddmmyyyy(dt, tz=None):
    """Дата/время в формате DD/MM/YYYY HH:MM."""
    if dt is None:
        return '—'
    if timezone.is_aware(dt) and tz:
        dt = dt.astimezone(tz)
    return dt.strftime('%d/%m/%Y %H:%M')


def format_date_ddmmyyyy(dt, tz=None):
    """Только дата DD/MM/YYYY."""
    if dt is None:
        return '—'
    if hasattr(dt, 'hour'):
        if timezone.is_aware(dt) and tz:
            dt = dt.astimezone(tz)
        return dt.strftime('%d/%m/%Y')
    return dt.strftime('%d/%m/%Y')


def get_datetime_context(request):
    """Контекст для шаблонов: UTC + локальная TZ, текстовый календарь."""
    user_zone = get_user_timezone(request)
    now_utc = timezone.now()
    now_local = now_utc.astimezone(user_zone)

    cal = calendar.TextCalendar(calendar.MONDAY)
    text_calendar = cal.formatmonth(now_local.year, now_local.month)

    return {
        'current_date_utc': now_utc.strftime('%d/%m/%Y'),
        'current_date_local': now_local.strftime('%d/%m/%Y'),
        'current_time_utc': now_utc.strftime('%H:%M:%S'),
        'current_time_local': now_local.strftime('%H:%M:%S'),
        'text_calendar': text_calendar,
        'user_timezone': str(user_zone),
        'common_timezones': COMMON_TIMEZONES,
        'user_zone': user_zone,
    }


def is_valid_timezone(name):
    """Проверка имени таймзоны через zoneinfo."""
    return name in available_timezones()
