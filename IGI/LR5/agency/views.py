"""Представления: авторизация и разграничение доступа."""

from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import DealForm, LoginForm, RegistrationForm, ReviewForm
from .models import Buyer, Deal, Employee, RealEstate, Review, UserProfile
from .roles import (
    ROLE_ADMIN,
    ROLE_ANONYMOUS,
    ROLE_CLIENT,
    ROLE_EMPLOYEE,
    admin_required,
    client_required,
    employee_required,
    get_client_buyer,
    get_user_role,
)
from .signals import GROUP_CLIENTS


def _auth_context(request, form, title):
    return {
        'form': form,
        'title': title,
        'user_role': get_user_role(request.user),
    }


def register_view(request):
    """Регистрация клиента."""
    if request.user.is_authenticated:
        return redirect('agency:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['full_name'].split()[0],
                    last_name=' '.join(
                        form.cleaned_data['full_name'].split()[1:],
                    ),
                )
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'role': UserProfile.ROLE_CLIENT},
                )
                Buyer.objects.create(
                    user=user,
                    full_name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email'],
                    birth_date=form.cleaned_data['birth_date'],
                )
                clients_group, _ = Group.objects.get_or_create(name=GROUP_CLIENTS)
                user.groups.add(clients_group)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('agency:home')
    else:
        form = RegistrationForm()

    return render(
        request,
        'agency/register.html',
        _auth_context(request, form, 'Регистрация'),
    )


def login_view(request):
    """Авторизация."""
    if request.user.is_authenticated:
        return redirect('agency:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(request, 'Вы успешно вошли в систему.')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('agency:home')
    else:
        form = LoginForm(request)

    return render(
        request,
        'agency/login.html',
        _auth_context(request, form, 'Вход'),
    )


@login_required
def logout_view(request):
    """Выход из системы."""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('agency:home')


def home_view(request):
    """Главная (заглушка до этапа 03)."""
    return render(request, 'agency/home.html', {
        'user_role': get_user_role(request.user),
    })


@client_required
def my_deals_view(request):
    """Сделки текущего клиента."""
    buyer = get_client_buyer(request.user)
    deals = Deal.objects.filter(buyer=buyer).select_related(
        'real_estate', 'employee',
    )
    return render(request, 'agency/my_deals.html', {
        'deals': deals,
        'user_role': ROLE_CLIENT,
    })


@client_required
def create_deal_view(request):
    """Оформление сделки клиентом."""
    buyer = get_client_buyer(request.user)
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            estate = form.cleaned_data['real_estate']
            employee = Employee.objects.first()
            if not employee:
                messages.error(request, 'Нет доступных сотрудников для оформления.')
            else:
                Deal.objects.create(
                    deal_type=form.cleaned_data['deal_type'],
                    real_estate=estate,
                    employee=employee,
                    buyer=buyer,
                    deal_date=date.today(),
                    amount=estate.price,
                )
                estate.status = (
                    RealEstate.STATUS_SOLD
                    if form.cleaned_data['deal_type'] == Deal.DEAL_SALE
                    else RealEstate.STATUS_RENTED
                )
                estate.save(update_fields=['status'])
                messages.success(request, 'Сделка оформлена.')
                return redirect('agency:my_deals')
    else:
        form = DealForm()

    return render(request, 'agency/create_deal.html', {
        'form': form,
        'user_role': ROLE_CLIENT,
    })

@login_required
def add_review_view(request):
    """Добавление отзыва (клиент или сотрудник; не аноним)."""
    role = get_user_role(request.user)
    if role == ROLE_ANONYMOUS:
        return redirect('agency:login')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if role == ROLE_CLIENT and hasattr(request.user, 'buyer_profile'):
                review.name = request.user.buyer_profile.full_name
            else:
                review.name = request.user.get_full_name() or request.user.username
            review.is_published = False
            review.save()
            messages.success(request, 'Отзыв отправлен на модерацию.')
            return redirect('agency:home')
    else:
        form = ReviewForm()

    return render(request, 'agency/add_review.html', {
        'form': form,
        'user_role': role,
    })


@employee_required
def employee_dashboard_view(request):
    """Панель сотрудника: его сделки, объекты, клиенты."""
    employee = request.user.employee_profile
    deals = Deal.objects.filter(employee=employee).select_related(
        'real_estate', 'buyer',
    )
    estate_ids = deals.values_list('real_estate_id', flat=True).distinct()
    buyer_ids = deals.values_list('buyer_id', flat=True).distinct()
    estates = RealEstate.objects.filter(id__in=estate_ids)
    buyers = Buyer.objects.filter(id__in=buyer_ids)

    return render(request, 'agency/employee_dashboard.html', {
        'deals': deals,
        'estates': estates,
        'buyers': buyers,
        'user_role': ROLE_EMPLOYEE,
    })


@admin_required
def admin_dashboard_view(request):
    """Заглушка панели администратора (полный CRUD — этап 03)."""
    return render(request, 'agency/admin_dashboard.html', {
        'user_role': ROLE_ADMIN,
    })
