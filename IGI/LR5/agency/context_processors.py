"""Контекст для шаблонов: роль, дата/время, таймзона."""

from .roles import get_user_role
from .timezone_utils import get_datetime_context


def user_role(request):
    """Добавляет user_role в каждый шаблон."""
    return {'user_role': get_user_role(request.user)}


def datetime_info(request):
    """UTC и локальное время, текстовый календарь (DD/MM/YYYY)."""
    return get_datetime_context(request)
