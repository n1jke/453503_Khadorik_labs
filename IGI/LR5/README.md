# RealEstateAgency - Агентство недвижимости (IGI LR5, вариант 26)

Django-приложение для автоматизации продажи и аренды недвижимости.

## Стек

- Python 3.11+, Django 4.2
- SQLite (локальная разработка) / PostgreSQL (Docker, Render)
- Gunicorn, WhiteNoise
- matplotlib, requests, pytest

## Быстрый старт (без Docker)

```bash
cd IGI/LR5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # при необходимости
python manage.py migrate
python manage.py load_demo_data
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/  
Админка: http://127.0.0.1:8000/admin/

## Docker (PostgreSQL локально)

```bash
docker compose up --build
```

После старта:

```bash
docker compose exec web python manage.py load_demo_data
docker compose exec web python manage.py createsuperuser
```

Сайт: http://127.0.0.1:8000/

## Тесты

```bash
pytest                 # покрытие ≥60%
pytest --no-cov -q     # быстрый прогон
```

## Деплой на Render.com

Подробная инструкция: **[docs/DEPLOY_RENDER.md](docs/DEPLOY_RENDER.md)**

Кратко:

1. Залить проект на GitHub (корень репозитория или `IGI/LR5` как Root Directory).
2. Создать PostgreSQL на Render, скопировать **Internal Database URL**.
3. Создать Web Service (Python 3), указать переменные окружения.
4. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. Start: `gunicorn RealEstateAgency.wsgi:application`

## Структура

```
IGI/LR5/
├── RealEstateAgency/   # settings, urls, wsgi
├── agency/             # приложение
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
├── docs/
│   ├── PROGRESS.md
│   ├── DEPLOY_RENDER.md
│   └── ER_DIAGRAM.md
└── manage.py
```

## Доступ для преподавателя (GitHub)

Добавить collaborator: **@AnnBsuir** (anzh52889@gmail.com)  
Settings > Collaborators > Add people

## Документация этапов

См. [docs/PROGRESS.md](docs/PROGRESS.md)
