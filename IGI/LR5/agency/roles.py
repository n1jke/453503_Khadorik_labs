"""User roles and access decorators."""

from functools import wraps

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

ROLE_ANONYMOUS = 'anonymous'
ROLE_CLIENT = 'client'
ROLE_EMPLOYEE = 'employee'
ROLE_ADMIN = 'admin'


def get_user_role(user):
    """
    Resolve role: anonymous, client, employee, admin.
    Superuser is admin; Employee profile is employee; otherwise client.
    """
    if user is None or not user.is_authenticated:
        return ROLE_ANONYMOUS
    if user.is_superuser:
        return ROLE_ADMIN
    if hasattr(user, 'employee_profile'):
        return ROLE_EMPLOYEE
    profile = getattr(user, 'profile', None)
    if profile and profile.role == 'employee':
        return ROLE_EMPLOYEE
    return ROLE_CLIENT


def get_client_buyer(user):
    """Buyer profile linked to the client user."""
    if get_user_role(user) != ROLE_CLIENT:
        return None
    return getattr(user, 'buyer_profile', None)


def _role_test(*allowed_roles):
    def check(user):
        return get_user_role(user) in allowed_roles

    return check


def role_required(*allowed_roles):
    """Decorator: allow only the given roles."""
    def decorator(view_func):
        @login_required
        @user_passes_test(
            _role_test(*allowed_roles),
            login_url='agency:login',
        )
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def client_required(view_func):
    """Registered client only."""
    return role_required(ROLE_CLIENT)(view_func)


def employee_required(view_func):
    """Employee only."""
    return role_required(ROLE_EMPLOYEE)(view_func)


def admin_required(view_func):
    """Superuser only."""
    return role_required(ROLE_ADMIN)(view_func)


def staff_or_admin_required(view_func):
    """Employee or administrator."""
    return role_required(ROLE_EMPLOYEE, ROLE_ADMIN)(view_func)


def login_required_api(view_func):
    """API views: authenticated users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied('Требуется авторизация.')
        return view_func(request, *args, **kwargs)

    return wrapper
