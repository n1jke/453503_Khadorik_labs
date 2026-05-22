# RealEstateAgency — Агентство недвижимости

## Стек

- Python 3.11+, Django 4.2
- SQLite (локальная разработка) / PostgreSQL (Docker, Render)
- Gunicorn, WhiteNoise
- matplotlib, requests, pytest

## Локальный запуск

```bash
cd IGI/LR5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Для SQLite оставьте DATABASE_URL пустым или удалите строку DATABASE_URL=

python manage.py migrate
python manage.py load_demo_data
python manage.py load_demo_data --ensure-images
python manage.py createsuperuser   # опционально
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/  
Админка: http://127.0.0.1:8000/admin/

Демо-логины после `load_demo_data`: сотрудники `employee1`..`employee12` / `employee123`.


| Путь | Назначение |
|------|------------|
| `templates/` | HTML-шаблоны |
| `static/css/` | CSS (отдаётся после `collectstatic`) |
| `media/` | PNG из `load_demo_data` (можно закоммитить для хостинга) |
| `staticfiles/` | **не в Git** - создаётся при деплое |
| `media/charts/` | **не в Git** - графики matplotlib |

Чтобы закоммитить картинки для хоста:

```bash
python manage.py load_demo_data
python manage.py load_demo_data --ensure-images
git add static/ templates/ media/
```

## Docker (PostgreSQL локально)

```bash
docker compose up --build
```

После старта:

```bash
docker compose exec web python manage.py load_demo_data
docker compose exec web python manage.py createsuperuser
```

## Тесты

```bash
pytest
pytest --no-cov -q
```
