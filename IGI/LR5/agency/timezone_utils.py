"""User timezone, DD/MM/YYYY format, text calendar."""

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
    Resolve timezone via zoneinfo:
    profile, then session, then X-Timezone header, then Europe/Minsk.
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
    """Datetime as DD/MM/YYYY HH:MM."""
    if dt is None:
        return 'N/A'
    if timezone.is_aware(dt) and tz:
        dt = dt.astimezone(tz)
    return dt.strftime('%d/%m/%Y %H:%M')


def format_date_ddmmyyyy(dt, tz=None):
    """Date only as DD/MM/YYYY."""
    if dt is None:
        return 'N/A'
    if hasattr(dt, 'hour'):
        if timezone.is_aware(dt) and tz:
            dt = dt.astimezone(tz)
        return dt.strftime('%d/%m/%Y')
    return dt.strftime('%d/%m/%Y')


def get_datetime_context(request):
    """Template context: UTC and local TZ, text calendar."""
    user_tz = get_user_timezone(request)
    now_utc = timezone.now()
    now_local = now_utc.astimezone(user_tz)

    cal = calendar.TextCalendar(calendar.MONDAY)
    text_calendar = cal.formatmonth(now_local.year, now_local.month)

    return {
        'current_date_utc': now_utc.strftime('%d/%m/%Y'),
        'current_date_local': now_local.strftime('%d/%m/%Y'),
        'current_time_utc': now_utc.strftime('%H:%M:%S'),
        'current_time_local': now_local.strftime('%H:%M:%S'),
        'text_calendar': text_calendar,
        'user_timezone': str(user_tz),
        'common_timezones': COMMON_TIMEZONES,
        'user_tz': user_tz,
    }


def is_valid_timezone(name):
    """Validate IANA timezone name via zoneinfo."""
    return name in available_timezones()
