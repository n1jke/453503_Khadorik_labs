# RealEstateAgency - Агентство недвижимости (IGI LR5, вариант 26)

Django-приложение для автоматизации продажи и аренды недвижимости.

## Стек

- Python 3.11+, Django 4.2
- SQLite (локально) / PostgreSQL (Docker, Render)
- Gunicorn, WhiteNoise
- matplotlib, requests, pytest

## Локальный запуск (без Docker)

```bash
cd IGI/LR5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Для SQLite оставьте DATABASE_URL пустым или удалите строку DATABASE_URL=
# Для Render PostgreSQL с ПК: External URL + DATABASE_SSL=true

python manage.py migrate
python manage.py load_demo_data
python manage.py load_demo_data --ensure-images
python manage.py createsuperuser   # опционально
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/  
Админка: http://127.0.0.1:8000/admin/

Демо-логины после `load_demo_data`: сотрудники `employee1`..`employee12` / `employee123`.

## Что в Git

| Путь | Назначение |
|------|------------|
| `templates/` | HTML-шаблоны |
| `static/css/` | CSS (отдаётся через WhiteNoise после `collectstatic`) |
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

После старта (если нужны демо-данные вручную):

```bash
docker compose exec web python manage.py load_demo_data
docker compose exec web python manage.py createsuperuser
```

`entrypoint.sh` уже выполняет `migrate`, `load_demo_data`, `--ensure-images`, `collectstatic`.

## Деплой на Render

1. Закоммитьте код (включая `static/`, `templates/`, при желании `media/`).
2. Web Service: Root Directory `IGI/LR5`, переменные из `.env.example.render`.
3. Build Command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

4. Start Command (Docker):

```bash
./entrypoint.sh
```

или без Docker:

```bash
gunicorn RealEstateAgency.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

При Docker-деплое `entrypoint.sh` сам загрузит демо-данные и PNG в БД/диск.

Первый раз в Shell (если БД пустая и без Docker entrypoint):

```bash
python manage.py load_demo_data
python manage.py createsuperuser
```

Подробнее: [docs/DEPLOY_RENDER.md](docs/DEPLOY_RENDER.md)

## Тесты

```bash
pytest
pytest --no-cov -q
```
