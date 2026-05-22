"""Template context: role, date/time, timezone."""

from .roles import get_user_role
from .timezone_utils import get_datetime_context


def user_role(request):
    """Expose user_role in every template."""
    return {'user_role': get_user_role(request.user)}


def datetime_info(request):
    """UTC and local time, text calendar (DD/MM/YYYY)."""
    return get_datetime_context(request)
