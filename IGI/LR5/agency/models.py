"""Модели приложения agency — агентство недвижимости."""

from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате +375 (29) XXX-XX-XX.',
)


def validate_age_18_plus(value):
    """Проверка возраста не менее 18 лет по дате рождения."""
    today = date.today()
    age = (
        today.year
        - value.year
        - ((today.month, today.day) < (value.month, value.day))
    )
    if age < 18:
        raise ValidationError('Возраст должен быть не менее 18 лет.')


class PropertyType(models.Model):
    """Вид недвижимости."""

    name = models.CharField('Название типа', max_length=100)
    description = models.TextField('Описание типа')

    class Meta:
        verbose_name = 'Вид недвижимости'
        verbose_name_plural = 'Виды недвижимости'
        ordering = ['name']

    def __str__(self):
        return self.name


class Owner(models.Model):
    """Владелец объекта недвижимости."""

    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[PHONE_VALIDATOR],
    )
    email = models.EmailField('Email')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class RealEstate(models.Model):
    """Объект недвижимости."""

    STATUS_AVAILABLE = 'available'
    STATUS_SOLD = 'sold'
    STATUS_RENTED = 'rented'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Доступен'),
        (STATUS_SOLD, 'Продан'),
        (STATUS_RENTED, 'Сдан в аренду'),
    ]

    code = models.CharField('Код объекта', max_length=50, unique=True)
    title = models.CharField('Заголовок', max_length=200)
    address = models.CharField('Адрес', max_length=300)
    area = models.DecimalField('Площадь, м²', max_digits=10, decimal_places=2)
    price = models.DecimalField('Стоимость', max_digits=14, decimal_places=2)
    rooms = models.PositiveIntegerField('Количество комнат')
    floor = models.PositiveIntegerField('Этаж')
    description = models.TextField('Описание')
    photo = models.ImageField('Фото', upload_to='real_estate/')
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name='primary_estates',
        verbose_name='Основной тип',
    )
    additional_types = models.ManyToManyField(
        PropertyType,
        blank=True,
        related_name='additional_estates',
        verbose_name='Дополнительные типы',
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name='properties',
        verbose_name='Владелец',
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} — {self.title}'


class Employee(models.Model):
    """Сотрудник агентства."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Пользователь',
    )
    department = models.CharField('Отдел', max_length=100)
    position = models.CharField('Должность', max_length=100)
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[PHONE_VALIDATOR],
    )
    birth_date = models.DateField(
        'Дата рождения',
        validators=[validate_age_18_plus],
    )
    photo = models.ImageField(
        'Фото',
        upload_to='employees/',
        blank=True,
    )
    hired_date = models.DateField('Дата приёма на работу')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['user__last_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Buyer(models.Model):
    """Покупатель или арендатор."""

    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[PHONE_VALIDATOR],
    )
    email = models.EmailField('Email')
    birth_date = models.DateField(
        'Дата рождения',
        validators=[validate_age_18_plus],
    )
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Покупатель/арендатор'
        verbose_name_plural = 'Покупатели/арендаторы'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Deal(models.Model):
    """Сделка по продаже или аренде."""

    DEAL_SALE = 'sale'
    DEAL_RENT = 'rent'
    DEAL_TYPE_CHOICES = [
        (DEAL_SALE, 'Продажа'),
        (DEAL_RENT, 'Аренда'),
    ]

    deal_type = models.CharField(
        'Тип сделки',
        max_length=10,
        choices=DEAL_TYPE_CHOICES,
    )
    real_estate = models.ForeignKey(
        RealEstate,
        on_delete=models.PROTECT,
        related_name='deals',
        verbose_name='Объект',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='deals',
        verbose_name='Сотрудник',
    )
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.PROTECT,
        related_name='deals',
        verbose_name='Покупатель',
    )
    deal_date = models.DateField('Дата сделки')
    amount = models.DecimalField('Сумма', max_digits=14, decimal_places=2)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
        ordering = ['-deal_date']

    def __str__(self):
        return f'{self.get_deal_type_display()} — {self.real_estate.code}'


class Article(models.Model):
    """Статья для главной страницы и раздела новостей."""

    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Полное содержание')
    short_content = models.CharField('Краткое содержание', max_length=300)
    image = models.ImageField('Изображение', upload_to='articles/')
    published_at = models.DateTimeField('Дата публикации')
    is_published = models.BooleanField('Опубликована', default=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    """Информация о компании (разделы сайта)."""

    SECTION_ABOUT = 'about'
    SECTION_CONTACTS = 'contacts'
    SECTION_REQUISITES = 'requisites'
    SECTION_PRIVACY = 'privacy'
    SECTION_CHOICES = [
        (SECTION_ABOUT, 'О компании'),
        (SECTION_CONTACTS, 'Контакты'),
        (SECTION_REQUISITES, 'Реквизиты'),
        (SECTION_PRIVACY, 'Политика конфиденциальности'),
    ]

    section = models.CharField('Раздел', max_length=50, choices=SECTION_CHOICES)
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст')
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'
        ordering = ['section', 'title']

    def __str__(self):
        return f'{self.get_section_display()}: {self.title}'


class GlossaryTerm(models.Model):
    """Термин словаря."""

    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Термин словаря'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['term']

    def __str__(self):
        return self.term


class Vacancy(models.Model):
    """Вакансия."""

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    salary = models.CharField('Зарплата', max_length=100, blank=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-is_active', 'title']

    def __str__(self):
        return self.title


class Review(models.Model):
    """Отзыв клиента."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField('Имя автора', max_length=100)
    rating = models.PositiveIntegerField(
        'Оценка',
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.rating})'


class PromoCode(models.Model):
    """Промокод или купон."""

    code = models.CharField('Промокод', max_length=50, unique=True)
    discount = models.DecimalField(
        'Скидка, %',
        max_digits=5,
        decimal_places=2,
    )
    description = models.TextField('Описание')
    valid_from = models.DateField('Действует с')
    valid_until = models.DateField('Действует до')
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['-valid_until']

    def __str__(self):
        return self.code
