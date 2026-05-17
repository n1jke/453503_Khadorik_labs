"""Фильтрация, поиск и сортировка списков."""

from decimal import Decimal, InvalidOperation

from django.db.models import Q


def filter_properties(queryset, params):
    """
    Поиск (?q=), фильтры (price_min, price_max, type, status, rooms),
    сортировка (?sort=price_asc|price_desc|area|date).
    Возвращает (queryset, context_dict для шаблона).
    """
    ctx = {
        'q': params.get('q', '').strip(),
        'price_min': params.get('price_min', ''),
        'price_max': params.get('price_max', ''),
        'type': params.get('type', ''),
        'status': params.get('status', ''),
        'rooms': params.get('rooms', ''),
        'sort': params.get('sort', 'date'),
    }

    q = ctx['q']
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q)
            | Q(address__icontains=q)
            | Q(description__icontains=q)
            | Q(code__icontains=q),
        )

    if ctx['price_min']:
        try:
            queryset = queryset.filter(price__gte=Decimal(ctx['price_min']))
        except (InvalidOperation, ValueError):
            pass

    if ctx['price_max']:
        try:
            queryset = queryset.filter(price__lte=Decimal(ctx['price_max']))
        except (InvalidOperation, ValueError):
            pass

    if ctx['type']:
        try:
            queryset = queryset.filter(property_type_id=int(ctx['type']))
        except (TypeError, ValueError):
            pass

    if ctx['status']:
        queryset = queryset.filter(status=ctx['status'])

    if ctx['rooms']:
        try:
            queryset = queryset.filter(rooms=int(ctx['rooms']))
        except (TypeError, ValueError):
            pass

    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'area': 'area',
        'area_desc': '-area',
        'date': '-created_at',
        'date_asc': 'created_at',
    }
    queryset = queryset.order_by(sort_map.get(ctx['sort'], '-created_at'))
    return queryset, ctx
