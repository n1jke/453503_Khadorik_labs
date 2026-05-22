# Деплой RealEstateAgency на Render.com

Пошаговый гайд для хостинга Django-приложения с **PostgreSQL**.

---

## Предварительные требования

- Аккаунт на [Render.com](https://render.com)
- Репозиторий на **GitHub** с проектом
- Доступ преподавателя: добавить **@AnnBsuir** (anzh52889@gmail.com) как collaborator

> Если весь репозиторий - монорепо, в настройках Web Service укажите  
> **Root Directory:** `IGI/LR5`

---

## Шаг 1. Подготовка репозитория

Убедитесь, что в Git есть:

- `requirements.txt` (Django, gunicorn, psycopg2-binary, dj-database-url, whitenoise, …)
- `manage.py`, `RealEstateAgency/`, `agency/`
- `Dockerfile` (опционально, для Docker-деплоя)
- `.env` **не** в репозитории (только `.env.example`)

```bash
git add .
git commit -m "Prepare RealEstateAgency for Render deploy"
git push origin <ваша-ветка>
```

---

## Шаг 2. PostgreSQL на Render

1. Dashboard > **New +** > **PostgreSQL**
2. Name: `realestate-db` (любое)
3. Region: **Frankfurt** (ближе к BY)
4. Plan: **Free**
5. **Create Database**
6. На вкладке **Info** скопируйте:
   - **Internal Database URL** - для Web Service в том же аккаунте Render  
     `postgresql://user:pass@host/dbname`
   - (External URL - только для подключения с вашего ПК)

---

## Шаг 3. Web Service

1. **New +** > **Web Service**
2. Подключить GitHub-репозиторий
3. Параметры:

| Поле | Значение |
|------|----------|
| Name | `real-estate-agency` (или своё) |
| Region | Frankfurt |
| Branch | `main` / `IGI_LR5` / ваша ветка |
| Root Directory | `IGI/LR5` (если проект в подпапке) |
| Runtime | **Python 3** |
| Build Command | см. ниже |
| Start Command | см. ниже |

**Build Command:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**

```bash
gunicorn RealEstateAgency.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

> Render подставляет переменную `$PORT` автоматически.

---

## Шаг 4. Переменные окружения

**Settings > Environment > Add Environment Variable**

| Key | Value | Обязательно |
|-----|-------|-------------|
| `SECRET_KEY` | Сгенерировать (см. ниже) | ✅ |
| `DATABASE_URL` | **Internal** URL из шага 2 | ✅ |
| `ALLOWED_HOSTS` | `real-estate-agency.onrender.com` (ваш домен без `https://`) | ✅ |
| `DEBUG` | `False` | ✅ |
| `LOG_LEVEL` | `INFO` | ✅ |
| `DATABASE_SSL` | `true` | ✅ (для External URL; для Internal часто можно `false`) |
| `OPENWEATHER_API_KEY` | ключ OpenWeatherMap | опционально |
| `WEATHER_CITY` | `Minsk` | опционально |
| `PYTHON_VERSION` | `3.11.9` | рекомендуется |

**Генерация SECRET_KEY** (локально):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

После добавления `ALLOWED_HOSTS` Django автоматически настроит `CSRF_TRUSTED_ORIGINS` для HTTPS.

---

## Шаг 5. Деплой

1. **Create Web Service**
2. Дождитесь зелёного статуса **Live** (первая сборка 5–15 мин)
3. Откройте URL: `https://<имя-сервиса>.onrender.com`

---

## Шаг 6. Данные и суперпользователь

В панели Render: **Shell** (или одноразовый job):

```bash
python manage.py load_demo_data
python manage.py createsuperuser
```

Либо только админа:

```bash
python manage.py createsuperuser --username admin --email admin@site.by
# ввести пароль интерактивно
```

---

## Шаг 7. Проверка

- [ ] Главная, новости, объекты, промокоды открываются
- [ ] Регистрация / вход
- [ ] Админка `/admin/`
- [ ] Статистика `/statistics/` (superuser)
- [ ] Статика (CSS) загружается (WhiteNoise)
- [ ] Логи в Render > **Logs**

---

## Docker локально (как на проде с PostgreSQL)

```bash
cd IGI/LR5
docker compose up --build
docker compose exec web python manage.py load_demo_data
docker compose exec web python manage.py createsuperuser
```

---

## Важные замечания

### Медиа-файлы (загрузки)

На бесплатном Render диск **эфемерный**: загруженные фото могут пропасть после перезапуска.  
Для продакшена используйте S3 / Render Persistent Disk или храните медиа вне сервера.

### Free tier

- Сервис «засыпает» после простоя: первый запрос может быть медленным (~30 с)
- PostgreSQL Free имеет лимиты по объёму

### Ошибки при сборке

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: psycopg2` | `psycopg2-binary` в requirements.txt |
| `DisallowedHost` | Добавить домен в `ALLOWED_HOSTS` |
| `CSRF verification failed` | Проверить HTTPS и `ALLOWED_HOSTS` |
| Статика не грузится | `collectstatic` в Build Command, WhiteNoise в settings |
| БД недоступна | Internal `DATABASE_URL`, не External |

---

## Схема окружений

```
Local (dev):        SQLite, DEBUG=True, runserver
Docker Compose:     PostgreSQL + Gunicorn
Render (prod):      PostgreSQL + Gunicorn + WhiteNoise
```

---

## Полезные ссылки

- [Render Django Deploy](https://render.com/docs/deploy-django)
- [Render PostgreSQL](https://render.com/docs/databases-postgresql)
- Прогресс проекта: [PROGRESS.md](PROGRESS.md)
