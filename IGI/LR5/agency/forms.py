"""Формы регистрации, авторизации, отзывов и сделок."""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Deal, RealEstate, Review
from .validators import (
    PHONE_INPUT_PATTERN,
    validate_age_18_plus_form,
    validate_non_whitespace,
    validate_phone,
)


def _html_attrs(**extra):
    """Базовые HTML5-атрибуты для полей."""
    attrs = {'class': 'form-field'}
    attrs.update(extra)
    return attrs


class RegistrationForm(forms.Form):
    """Регистрация клиента."""

    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs=_html_attrs(required='required', minlength='3')),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs=_html_attrs(required='required', type='email')),
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(
            attrs=_html_attrs(required='required', minlength='8'),
        ),
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs=_html_attrs(required='required')),
    )
    full_name = forms.CharField(
        label='ФИО',
        max_length=200,
        widget=forms.TextInput(attrs=_html_attrs(required='required')),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs=_html_attrs(
            required='required',
            pattern=PHONE_INPUT_PATTERN,
            placeholder='+375 (29) 123-45-67',
            title='+375 (29) XXX-XX-XX',
        )),
    )
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(
            attrs=_html_attrs(required='required', type='date'),
            format='%Y-%m-%d',
        ),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        validate_non_whitespace(username)
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        validate_non_whitespace(full_name)
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        validate_phone(phone)
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_age_18_plus_form(birth_date)
        return birth_date

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password_confirm = cleaned.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error(
                'password_confirm',
                ValidationError('Пароли не совпадают.'),
            )
        return cleaned


class LoginForm(forms.Form):
    """Авторизация."""

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs=_html_attrs(required='required')),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs=_html_attrs(required='required')),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '').strip()
        password = cleaned.get('password')
        if username and password:
            user = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if user is None:
                raise ValidationError('Неверный логин или пароль.')
            self.user = user
        return cleaned


class ReviewForm(forms.ModelForm):
    """Добавление отзыва."""

    class Meta:
        model = Review
        fields = ('rating', 'text')
        widgets = {
            'rating': forms.Select(attrs=_html_attrs(
                required='required',
            )),
            'text': forms.Textarea(attrs=_html_attrs(
                required='required',
                rows='5',
                minlength='10',
            )),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        validate_non_whitespace(text)
        if len(text) < 10:
            raise ValidationError('Текст отзыва должен быть не короче 10 символов.')
        return text

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Оценка должна быть от 1 до 5.')
        return rating


class DealForm(forms.ModelForm):
    """Оформление сделки клиентом."""

    class Meta:
        model = Deal
        fields = ('real_estate', 'deal_type')
        widgets = {
            'real_estate': forms.Select(attrs=_html_attrs(required='required')),
            'deal_type': forms.Select(attrs=_html_attrs(required='required')),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['real_estate'].queryset = RealEstate.objects.filter(
            status=RealEstate.STATUS_AVAILABLE,
        )

    def clean_real_estate(self):
        estate = self.cleaned_data['real_estate']
        if estate.status != RealEstate.STATUS_AVAILABLE:
            raise ValidationError('Объект недоступен для сделки.')
        return estate


class RealEstateForm(forms.ModelForm):
    """CRUD объекта недвижимости (админ)."""

    class Meta:
        model = RealEstate
        fields = (
            'code', 'title', 'address', 'area', 'price', 'rooms', 'floor',
            'description', 'photo', 'property_type', 'additional_types',
            'owner', 'status',
        )
        widgets = {
            'code': forms.TextInput(attrs=_html_attrs(required='required')),
            'title': forms.TextInput(attrs=_html_attrs(required='required')),
            'address': forms.TextInput(attrs=_html_attrs(required='required')),
            'area': forms.NumberInput(attrs=_html_attrs(required='required', min='0.01', step='0.01')),
            'price': forms.NumberInput(attrs=_html_attrs(required='required', min='0.01', step='0.01')),
            'rooms': forms.NumberInput(attrs=_html_attrs(required='required', min='1')),
            'floor': forms.NumberInput(attrs=_html_attrs(required='required', min='1')),
            'description': forms.Textarea(attrs=_html_attrs(required='required', rows='5')),
            'photo': forms.FileInput(attrs=_html_attrs()),
            'property_type': forms.Select(attrs=_html_attrs(required='required')),
            'additional_types': forms.CheckboxSelectMultiple(),
            'owner': forms.Select(attrs=_html_attrs(required='required')),
            'status': forms.Select(attrs=_html_attrs(required='required')),
        }

    def clean_code(self):
        code = self.cleaned_data['code'].strip()
        validate_non_whitespace(code)
        return code

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        validate_non_whitespace(title)
        return title

    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        validate_non_whitespace(address)
        return address


class DealManageForm(forms.ModelForm):
    """Редактирование сделки (сотрудник / админ)."""

    class Meta:
        model = Deal
        fields = (
            'deal_type', 'real_estate', 'employee', 'buyer',
            'deal_date', 'amount',
        )
        widgets = {
            'deal_type': forms.Select(attrs=_html_attrs(required='required')),
            'real_estate': forms.Select(attrs=_html_attrs(required='required')),
            'employee': forms.Select(attrs=_html_attrs(required='required')),
            'buyer': forms.Select(attrs=_html_attrs(required='required')),
            'deal_date': forms.DateInput(
                attrs=_html_attrs(required='required', type='date'),
                format='%Y-%m-%d',
            ),
            'amount': forms.NumberInput(
                attrs=_html_attrs(required='required', min='0.01', step='0.01'),
            ),
        }

    def __init__(self, *args, employee_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        if employee_only:
            self.fields.pop('employee', None)


class DealAdminForm(DealManageForm):
    """Полная форма сделки для администратора."""

    pass
