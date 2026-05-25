# RealEstateAgency — Агентство Недвижимости

**RealEstateAgency** — веб приложение для управления объектами недвижимости, сделками купли-продажи/аренды, сотрудниками и клиентами и интеграцией с внешними API.

## Key points

- [x]  **Управление недвижимостью** — каталог объектов с фото, описанием, координатами  
- [x] **CRM для сотрудников** — управление сделками, клиентами, статистика продаж  
- [x] **Гибкая система ролей** — клиент, сотрудник, администратор с разными правами доступа  
- [x] **Интеграция с API** — погода (OpenWeatherMap), курсы валют, геокодирование (Nominatim)  
- [x] **Аналитика** — графики сделок, статистика продаж (matplotlib)  
- [x] **Отзывы и рейтинги** — система оценок от клиентов  
- [x] **Демо-данные** — встроенная загрузка тестовых объектов и пользователей  

---

## Technologies

| Слой | Технология |
| ------ | ------------ |
| **Backend** | Django 4.2/Python 3.11+ |
| **Frontend** | Django Templates, HTML/CSS/JS |
| **Db** | SQLite/ PostgreSQL |
| **API** | OpenWeatherMap, ExchangeRate-API, Nominatim |
| **Testing** | pytest, pytest-django, pytest-cov |
| **Deploy** | Docker, Render.com |

---

## Layout & architecture

## Структура проекта

```Python
IGI/LR5/
├── agency/              
│   ├── models.py        
│   ├── views.py         
│   ├── services.py      
│   ├── forms.py         
│   ├── roles.py         
│   └── tests/           
├── templates/           
├── static/              
├── media/               
├── docs/                
├── RealEstateAgency/    
├── .env.example         
├── requirements.txt     
├── Dockerfile           
└── docker-compose.yml   
```

### Модели данных

- **Пользователи & Профили** — система ролей, аутентификация
- **Недвижимость** — объекты с фото, координатами, статусом
- **Сделки** — связь объект + сотрудник + клиент + статус
- **Контент** — новости, отзывы, словарь терминов, вакансии
- **Компания** — информация, промокоды, контакты

**→ [Схема данных в диаграмме](docs/ER_DIAGRAM.md)**

### Права пользователей

| Роль | Права |
| ------ | ------- |
| **Unauthorized** | Просмотр каталога, новостей, контактов |
| **Client** | + Создание профиля, просмотр своих сделок, работа с отзывами |
| **Employee** | + Управление объектами, создание сделок и их аналитика |
| **Admin** | Полный доступ, панель администратора |

### Основной компонент

```Python
agency/
├── models.py         # Модели данных
├── views.py          # Представления
├── services.py       # Интеграция с внешними сервисами
├── forms.py          # Формы пользовательского ввода
├── roles.py          # Декораторы для проверки прав доступа
├── charts.py         # Построение графиков с matplotlib
└── tests/            # unit tests
```

---

## Usage

### Локально

```bash
cd IGI/LR5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example.local .env
python manage.py migrate
python manage.py load_demo_data
python manage.py runserver
```

**Сайт:** <http://127.0.0.1:8000/>  
**Админ:** <http://127.0.0.1:8000/admin/>  

---

## Testing

```bash
pytest
```

**Покрытие:** 80% кода покрыто тестами (models, views, forms, services, validators)

---

## Env-s

Используйте `.env.example.local` для локальной разработки:

```bash
cp .env.example.local .env
```

Для Render.com: `.env.example.render`

---
