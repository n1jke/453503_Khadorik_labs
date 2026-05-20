"""Генерация графиков matplotlib (Agg) на данных из БД."""

import os
from datetime import datetime

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncMonth

from .models import Deal, PropertyType

DEAL_TYPE_LABELS = {
    'sale': 'Продажа',
    'rent': 'Аренда',
}


def _save_chart(fig, prefix):
    """Сохранить figure в MEDIA_ROOT/charts/."""
    filename = f'{prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    rel_path = os.path.join('charts', filename)
    filepath = os.path.join(settings.MEDIA_ROOT, rel_path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig.savefig(filepath, dpi=100, bbox_inches='tight')
    plt.close(fig)
    return rel_path.replace('\\', '/')


def generate_deals_by_type_chart():
    """Столбчатая диаграмма: сделки по типам."""
    rows = Deal.objects.values('deal_type').annotate(count=Count('id'))
    labels = [DEAL_TYPE_LABELS.get(r['deal_type'], r['deal_type']) for r in rows]
    counts = [r['count'] for r in rows]
    if not counts:
        labels, counts = ['Нет данных'], [0]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, counts, color=['#4CAF50', '#2196F3'][: len(labels)])
    ax.set_title('Сделки по типам')
    ax.set_xlabel('Тип сделки')
    ax.set_ylabel('Количество')
    return _save_chart(fig, 'chart_deals')


def generate_deals_over_time_chart():
    """Линейный график: сделки по месяцам."""
    rows = (
        Deal.objects.annotate(month=TruncMonth('deal_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    months = [
        r['month'].strftime('%Y-%m') if r['month'] else '—'
        for r in rows
    ]
    counts = [r['count'] for r in rows]
    if not months:
        months, counts = ['—'], [0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months, counts, marker='o', color='#FF5722', linewidth=2)
    ax.set_title('Сделки по месяцам')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Количество сделок')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    return _save_chart(fig, 'chart_timeline')


def generate_property_types_chart():
    """Круговая диаграмма: объекты по типам недвижимости."""
    types = PropertyType.objects.annotate(
        count=Count('primary_estates'),
    ).order_by('-count')
    labels = [t.name for t in types]
    counts = [t.count for t in types]
    if not counts or sum(counts) == 0:
        labels, counts = ['Нет данных'], [1]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Распределение объектов по типам')
    return _save_chart(fig, 'chart_types')


def generate_all_charts():
    """Сгенерировать все графики для страницы статистики."""
    return {
        'deals_by_type': generate_deals_by_type_chart(),
        'deals_timeline': generate_deals_over_time_chart(),
        'property_types': generate_property_types_chart(),
    }
