# Прогресс: RealEstateAgency (вариант 26)

| Этап | Файл | Статус |
|------|------|--------|
| 00 | `temp/00_project_overview.txt` | - |
| 01 | `temp/01_models_and_admin.txt` | done |
| 02 | `temp/02_auth_and_validation.txt` | done |
| 03 | `temp/03_urls_views_templates.txt` | done |
| 04 | `temp/04_api_statistics_timezone.txt` | done |
| 05 | `temp/05_additional_concurrency.txt` | skipped |
| 06 | `temp/06_logging_testing.txt` | done |
| **07** | **`temp/07_docker_deploy.txt`** | **done** |

---

## Этап 07: Docker, deploy, GitHub

### Docker

- `Dockerfile` - Python 3.11-slim, gunicorn, `entrypoint.sh` (migrate + collectstatic)
- `docker-compose.yml` - **web** + **PostgreSQL 15**
- `.dockerignore`

### Settings (prod)

- `DATABASE_URL` uses PostgreSQL (`dj-database-url`)
- without `DATABASE_URL` uses SQLite (local dev)
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from env
- **WhiteNoise** for static files
- `CSRF_TRUSTED_ORIGINS` for HTTPS on Render

### Files

- `README.md` - quick start
- `docs/DEPLOY_RENDER.md` - Render.com guide
- `render.yaml` - optional Blueprint
- `.env.example` - environment variables

### Commands

```bash
# Docker
docker compose up --build

# Render (see DEPLOY_RENDER.md)
# Root Directory: IGI/LR5
```

### GitHub

Add collaborator: **@AnnBsuir** (anzh52889@gmail.com)

---

**Project complete** (stage 05 asyncio skipped by agreement).
