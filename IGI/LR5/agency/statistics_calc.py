"""Statistics for the admin dashboard."""

from datetime import date, timedelta
from statistics import mean, median, mode, multimode

from django.db.models import Avg, Count, Sum
from django.utils import timezone

from .models import Buyer, Deal, Employee, PropertyType, RealEstate
from .validators import calculate_age


def _safe_mode(values):
    """Mode; if multiple modes exist, use multimode."""
    if not values:
        return None
    try:
        return mode(values)
    except ValueError:
        modes = multimode(values)
        return modes[0] if len(modes) == 1 else modes


def compute_statistics():
    """Collect all metrics for statistics.html."""
    estates_alpha = RealEstate.objects.order_by('title')
    buyers_alpha = Buyer.objects.order_by('full_name')

    amounts = list(
        Deal.objects.values_list('amount', flat=True),
    )
    float_amounts = [float(a) for a in amounts]

    total_deals_sum = sum(float_amounts) if float_amounts else 0
    deal_stats = {
        'count': len(float_amounts),
        'mean': mean(float_amounts) if float_amounts else 0,
        'median': median(float_amounts) if float_amounts else 0,
        'mode': _safe_mode(float_amounts),
    }

    ages = [
        calculate_age(b.birth_date)
        for b in Buyer.objects.exclude(birth_date__isnull=True)
    ]
    age_stats = {
        'mean': mean(ages) if ages else 0,
        'median': median(ages) if ages else 0,
        'count': len(ages),
    }

    popular_type = (
        PropertyType.objects.annotate(
            deal_count=Count('primary_estates__deals'),
        )
        .order_by('-deal_count')
        .first()
    )

    profitable_type = (
        PropertyType.objects.annotate(
            total_amount=Sum('primary_estates__deals__amount'),
        )
        .order_by('-total_amount')
        .first()
    )

    employees_stats = list(
        Employee.objects.annotate(
            deal_count=Count('deals'),
            total_amount=Sum('deals__amount'),
        )
        .select_related('user')
        .order_by('-deal_count'),
    )

    deals_by_type = list(
        Deal.objects.values('deal_type')
        .annotate(count=Count('id'), total=Sum('amount')),
    )

    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)

    deals_last_month = Deal.objects.filter(deal_date__gte=month_ago).count()
    deals_last_year = Deal.objects.filter(deal_date__gte=year_ago).count()
    avg_check = (
        Deal.objects.aggregate(avg=Avg('amount'))['avg'] or 0
    )

    return {
        'estates_alpha': estates_alpha,
        'buyers_alpha': buyers_alpha,
        'total_deals_sum': total_deals_sum,
        'deal_stats': deal_stats,
        'age_stats': age_stats,
        'popular_type': popular_type,
        'profitable_type': profitable_type,
        'employees_stats': employees_stats,
        'deals_by_type': deals_by_type,
        'deals_last_month': deals_last_month,
        'deals_last_year': deals_last_year,
        'avg_check': avg_check,
    }
