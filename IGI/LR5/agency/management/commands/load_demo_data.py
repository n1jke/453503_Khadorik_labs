"""Management-команда: наполнение БД демонстрационными данными (10+ записей в каждой таблице)."""

import random
from datetime import date, datetime, timedelta
from decimal import Decimal
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from agency.models import (
    Article,
    Buyer,
    CompanyInfo,
    Deal,
    Employee,
    GlossaryTerm,
    Owner,
    PromoCode,
    PropertyType,
    RealEstate,
    Review,
    UserProfile,
    Vacancy,
)

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None


def phone_number(index):
    """Телефон в формате +375 (29) XXX-XX-XX."""
    part = 100 + index
    return f'+375 (29) {part:03d}-{index % 100:02d}-{index % 100:02d}'


def make_image(name, color):
    """Создать простое PNG-изображение для ImageField."""
    if Image is None:
        return ContentFile(b'', name=f'{name}.png')
    img = Image.new('RGB', (400, 300), color=color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 380, 280], outline='white', width=3)
    draw.text((40, 130), name[:20], fill='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{name}.png')


class Command(BaseCommand):
    help = 'Загружает демонстрационные данные (минимум 10 записей в каждой таблице).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Удалить существующие данные agency перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self._flush_data()

        if PropertyType.objects.exists():
            self.stdout.write(self.style.WARNING('Данные уже есть. Используйте --flush.'))
            return

        property_types = self._create_property_types()
        owners = self._create_owners()
        estates = self._create_real_estates(property_types, owners)
        employees = self._create_employees()
        buyers = self._create_buyers()
        self._create_deals(estates, employees, buyers)
        self._create_articles()
        self._create_company_info()
        self._create_glossary()
        self._create_vacancies()
        self._create_reviews()
        self._create_promo_codes()

        from django.core.management import call_command
        call_command('sync_profiles')

        self.stdout.write(self.style.SUCCESS('Демо-данные успешно загружены.'))

    def _flush_data(self):
        models_order = [
            Deal, Review, PromoCode, Article, Vacancy, GlossaryTerm,
            CompanyInfo, RealEstate, Employee, Buyer, UserProfile,
            Owner, PropertyType,
        ]
        for model in models_order:
            model.objects.all().delete()
        User.objects.filter(username__startswith='employee').delete()
        self.stdout.write('Старые данные удалены.')

    def _create_property_types(self):
        names = [
            ('Квартира', 'Жилые помещения в многоквартирных домах.'),
            ('Дом', 'Отдельно стоящие жилые здания.'),
            ('Офис', 'Коммерческие помещения для бизнеса.'),
            ('Участок', 'Земельные наделы под застройку.'),
            ('Склад', 'Производственно-складские помещения.'),
            ('Таунхаус', 'Блокированная застройка.'),
            ('Студия', 'Квартиры с открытой планировкой.'),
            ('Пентхаус', 'Элитное жильё на верхних этажах.'),
            ('Гараж', 'Парковочные места и боксы.'),
            ('Торговое помещение', 'Ритейл и шоурумы.'),
            ('Коттедж', 'Загородное жильё премиум-класса.'),
            ('Лофт', 'Помещения в стиле open space.'),
        ]
        result = []
        for name, desc in names:
            result.append(PropertyType.objects.create(name=name, description=desc))
        return result

    def _create_owners(self):
        owners = []
        for i in range(1, 13):
            owners.append(
                Owner.objects.create(
                    full_name=f'Владелец {i} Иванов',
                    phone=phone_number(i),
                    email=f'owner{i}@example.com',
                )
            )
        return owners

    def _create_real_estates(self, property_types, owners):
        statuses = [
            RealEstate.STATUS_AVAILABLE,
            RealEstate.STATUS_SOLD,
            RealEstate.STATUS_RENTED,
        ]
        colors = [
            '#2c3e50', '#8e44ad', '#27ae60', '#c0392b',
            '#2980b9', '#d35400', '#16a085', '#7f8c8d',
            '#34495e', '#e67e22', '#1abc9c', '#9b59b6',
        ]
        estates = []
        for i in range(1, 13):
            pt = property_types[i % len(property_types)]
            owner = owners[i % len(owners)]
            estate = RealEstate(
                code=f'RE-{i:04d}',
                title=f'Объект {i}: {pt.name}',
                address=f'г. Минск, ул. Примерная, {i}',
                area=Decimal(str(30 + i * 5 + random.randint(0, 20))),
                price=Decimal(str(50000 + i * 12000)),
                rooms=(i % 4) + 1,
                floor=(i % 12) + 1,
                description=f'Подробное описание объекта {i}.',
                property_type=pt,
                owner=owner,
                status=statuses[i % len(statuses)],
            )
            estate.photo.save(
                f'estate_{i}.png',
                make_image(f'RE-{i}', colors[i % len(colors)]),
                save=False,
            )
            estate.save()
            if i % 3 == 0:
                extra = property_types[(i + 1) % len(property_types)]
                estate.additional_types.add(extra)
            estates.append(estate)
        return estates

    def _create_employees(self):
        departments = ['Продажи', 'Аренда', 'Маркетинг', 'Юридический отдел']
        positions = ['Риелтор', 'Менеджер', 'Аналитик', 'Юрист']
        employees = []
        for i in range(1, 13):
            user = User.objects.create_user(
                username=f'employee{i}',
                password='employee123',
                first_name=f'Сотрудник{i}',
                last_name='Петров',
                email=f'employee{i}@agency.by',
            )
            emp = Employee(
                user=user,
                department=departments[i % len(departments)],
                position=positions[i % len(positions)],
                phone=phone_number(20 + i),
                birth_date=date(1980 + (i % 15), 5, 15),
                hired_date=date(2015 + (i % 8), 1, 10),
            )
            if i % 2 == 0:
                emp.photo.save(
                    f'emp_{i}.png',
                    make_image(f'EMP{i}', '#3498db'),
                    save=False,
                )
            emp.save()
            employees.append(emp)
        return employees

    def _create_buyers(self):
        buyers = []
        for i in range(1, 13):
            buyers.append(
                Buyer.objects.create(
                    full_name=f'Покупатель {i} Сидоров',
                    phone=phone_number(40 + i),
                    email=f'buyer{i}@mail.by',
                    birth_date=date(1990 + (i % 10), 3, 20),
                )
            )
        return buyers

    def _create_deals(self, estates, employees, buyers):
        today = date.today()
        for i in range(12):
            Deal.objects.create(
                deal_type=Deal.DEAL_SALE if i % 2 == 0 else Deal.DEAL_RENT,
                real_estate=estates[i % len(estates)],
                employee=employees[i % len(employees)],
                buyer=buyers[i % len(buyers)],
                deal_date=today - timedelta(days=i * 10),
                amount=estates[i % len(estates)].price * Decimal('0.95'),
            )

    def _create_articles(self):
        now = timezone.now()
        for i in range(1, 13):
            article = Article(
                title=f'Новость агентства №{i}',
                content=f'Полный текст новости номер {i}.' * 5,
                short_content=f'Кратко: важная новость номер {i}.',
                published_at=now - timedelta(days=i),
                is_published=i % 4 != 0,
            )
            article.image.save(
                f'article_{i}.png',
                make_image(f'NEWS{i}', '#e74c3c'),
                save=False,
            )
            article.save()

    def _create_company_info(self):
        sections_data = [
            (CompanyInfo.SECTION_ABOUT, 'О нас', 'Агентство недвижимости с 2010 года.'),
            (CompanyInfo.SECTION_ABOUT, 'Миссия', 'Помогаем найти идеальное жильё.'),
            (CompanyInfo.SECTION_CONTACTS, 'Телефон', '+375 (29) 100-00-01'),
            (CompanyInfo.SECTION_CONTACTS, 'Email', 'info@realestate.by'),
            (CompanyInfo.SECTION_CONTACTS, 'Адрес офиса', 'г. Минск, пр. Независимости, 1'),
            (CompanyInfo.SECTION_REQUISITES, 'УНП', '123456789'),
            (CompanyInfo.SECTION_REQUISITES, 'Банк', 'ОАО «Банк»'),
            (CompanyInfo.SECTION_REQUISITES, 'Р/с', 'BY00BANK00000000000000'),
            (CompanyInfo.SECTION_PRIVACY, 'Политика', 'Текст политики конфиденциальности.'),
        ]
        for section, title, content in sections_data:
            CompanyInfo.objects.create(section=section, title=title, content=content)
        for i in range(10, 13):
            CompanyInfo.objects.create(
                section=CompanyInfo.SECTION_ABOUT,
                title=f'Доп. блок {i}',
                content=f'Дополнительная информация блок {i}.',
            )

    def _create_glossary(self):
        terms = [
            ('Риелтор', 'Специалист по операциям с недвижимостью.'),
            ('Депозит', 'Залог при аренде помещения.'),
            ('Ипотека', 'Кредит на покупку жилья.'),
            ('Кадастр', 'Государственный учёт объектов.'),
            ('Эскроу', 'Безопасная схема расчётов.'),
            ('Аренда', 'Временное пользование объектом.'),
            ('Залог', 'Обеспечение обязательств имуществом.'),
            ('Оценка', 'Определение рыночной стоимости.'),
            ('Договор', 'Юридическое соглашение сторон.'),
            ('Комиссия', 'Вознаграждение агентства.'),
            ('Ликвидность', 'Скорость продажи объекта.'),
            ('Пентхаус', 'Квартира на верхнем этаже.'),
        ]
        for term, definition in terms:
            GlossaryTerm.objects.create(term=term, definition=definition)

    def _create_vacancies(self):
        titles = [
            'Риелтор', 'Менеджер по аренде', 'Маркетолог', 'Юрист',
            'Аналитик рынка', 'Администратор', 'Фотограф объектов',
            'SMM-специалист', 'Бухгалтер', 'HR-менеджер',
            'Курьер документов', 'Стажёр отдела продаж',
        ]
        for i, title in enumerate(titles):
            Vacancy.objects.create(
                title=title,
                description=f'Требования к вакансии «{title}».',
                salary=f'{800 + i * 100} BYN',
                is_active=i % 5 != 4,
            )

    def _create_reviews(self):
        for i in range(1, 13):
            Review.objects.create(
                name=f'Клиент {i}',
                rating=(i % 5) + 1,
                text=f'Отзыв клиента {i} о работе агентства.',
                is_published=i % 3 != 0,
            )

    def _create_promo_codes(self):
        today = date.today()
        for i in range(1, 13):
            PromoCode.objects.create(
                code=f'PROMO{i:02d}',
                discount=Decimal(str(5 + i)),
                description=f'Скидка {5 + i}% на услуги агентства.',
                valid_from=today - timedelta(days=30 + i),
                valid_until=today + timedelta(days=30 - i * 2),
                is_active=i % 4 != 3,
            )
