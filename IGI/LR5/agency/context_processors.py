"""Контекст для шаблонов: роль пользователя."""

from .roles import get_user_role


def user_role(request):
    """Добавляет user_role в каждый шаблон."""
    return {'user_role': get_user_role(request.user)}
