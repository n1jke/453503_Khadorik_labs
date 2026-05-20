"""Интеграция с внешними API (requests)."""

import logging
from urllib.parse import quote

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = getattr(settings, 'API_REQUEST_TIMEOUT', 5)

DEFAULT_WEATHER = {
    'city': 'Минск',
    'temperature': '—',
    'description': 'Данные недоступны',
    'icon': '',
    'humidity': '—',
    'from_api': False,
}

DEFAULT_RATES = {
    'base': 'BYN',
    'USD': 3.25,
    'EUR': 3.55,
    'USD_per_byn': 0.31,
    'EUR_per_byn': 0.28,
    'from_api': False,
}


def get_weather(city=None):
    """
    OpenWeatherMap — текущая погода.
    Ключ: OPENWEATHER_API_KEY в .env / settings.
    """
    city = city or getattr(settings, 'WEATHER_CITY', 'Minsk')
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '') or ''
    if not api_key:
        logger.warning('OPENWEATHER_API_KEY не задан')
        result = DEFAULT_WEATHER.copy()
        result['city'] = city
        return result

    url = (
        'https://api.openweathermap.org/data/2.5/weather'
        f'?q={quote(city)}&appid={api_key}&units=metric&lang=ru'
    )
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data.get('name', city),
            'temperature': round(data['main']['temp'], 1),
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main'].get('humidity', '—'),
            'from_api': True,
        }
    except (requests.RequestException, KeyError, TypeError) as exc:
        logger.error('Ошибка OpenWeatherMap: %s', exc)
        result = DEFAULT_WEATHER.copy()
        result['city'] = city
        return result


def get_exchange_rates():
    """ExchangeRate-API — курсы USD/EUR к BYN."""
    url = 'https://api.exchangerate-api.com/v4/latest/BYN'
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        rates = response.json().get('rates', {})
        usd = rates.get('USD')
        eur = rates.get('EUR')
        if not usd or not eur:
            raise ValueError('Неполный ответ API')
        return {
            'base': 'BYN',
            'USD': round(1 / usd, 4) if usd else None,
            'EUR': round(1 / eur, 4) if eur else None,
            'USD_per_byn': usd,
            'EUR_per_byn': eur,
            'from_api': True,
        }
    except (requests.RequestException, ValueError, TypeError) as exc:
        logger.error('Ошибка ExchangeRate-API: %s', exc)
        return DEFAULT_RATES.copy()


def geocode_address(address):
    """
    Nominatim (OpenStreetMap) — координаты по адресу.
    Дополнительный гео-API для карточки объекта.
    """
    url = (
        'https://nominatim.openstreetmap.org/search'
        f'?q={quote(address)}&format=json&limit=1'
    )
    headers = {'User-Agent': 'RealEstateAgency/1.0 (educational)'}
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
        item = data[0]
        return {
            'lat': item.get('lat'),
            'lon': item.get('lon'),
            'display_name': item.get('display_name', address),
            'from_api': True,
        }
    except (requests.RequestException, KeyError, TypeError) as exc:
        logger.error('Ошибка Nominatim: %s', exc)
        return None
