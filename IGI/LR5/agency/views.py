"""Function-based views: pages, CRUD, authentication."""

import logging
from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .charts import generate_all_charts
from .services import geocode_address, get_exchange_rates, get_weather
from .statistics_calc import compute_statistics
from .timezone_utils import format_datetime_ddmmyyyy, get_user_timezone, is_valid_timezone

from .forms import (
    DealAdminForm,
    DealForm,
    DealManageForm,
    LoginForm,
    RealEstateForm,
    RegistrationForm,
    ReviewForm,
)
from .models import (
    Article,
    Buyer,
    CompanyInfo,
    Deal,
    Employee,
    GlossaryTerm,
    PromoCode,
    PropertyType,
    RealEstate,
    Review,
    UserProfile,
    Vacancy,
)
from .querysets import filter_properties
from .roles import (
    ROLE_ADMIN,
    ROLE_CLIENT,
    ROLE_EMPLOYEE,
    admin_required,
    client_required,
    employee_required,
    get_client_buyer,
    get_user_role,
    login_required_api,
)
from .signals import GROUP_CLIENTS

logger = logging.getLogger('agency')


def _page(request, template, extra=None):
    """Base page context."""
    ctx = {'user_role': get_user_role(request.user)}
    if extra:
        ctx.update(extra)
    return render(request, template, ctx)


# --- Authentication ---


def register_view(request):
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
                    last_name=' '.join(form.cleaned_data['full_name'].split()[1:]),
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
            logger.info('New user registered: %s', user.username)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('agency:home')
        logger.warning('Registration failed: %s', form.errors)
    else:
        form = RegistrationForm()
    return _page(request, 'agency/register.html', {'form': form, 'title': 'Регистрация'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('agency:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            logger.info('User %s logged in successfully', form.user.username)
            messages.success(request, 'Вы успешно вошли в систему.')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('agency:home')
        username = request.POST.get('username', '')
        logger.warning('Failed login attempt for username: %s', username)
    else:
        form = LoginForm(request)
    return _page(request, 'agency/login.html', {'form': form, 'title': 'Вход'})


@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logger.info('User %s logged out', request.user.username)
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('agency:home')


# --- Public pages ---


def home_view(request):
    article = (
        Article.objects.filter(is_published=True)
        .order_by('-published_at')
        .first()
    )
    weather = get_weather()
    return _page(request, 'agency/home.html', {
        'latest_article': article,
        'weather': weather,
    })


def about_view(request):
    sections = CompanyInfo.objects.filter(section=CompanyInfo.SECTION_ABOUT)
    return _page(request, 'agency/about.html', {'sections': sections})


def news_list_view(request):
    articles = Article.objects.filter(is_published=True).order_by('-published_at')
    return _page(request, 'agency/news_list.html', {'articles': articles})


def news_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk, is_published=True)
    return _page(request, 'agency/news_detail.html', {'article': article})


def glossary_view(request):
    terms = GlossaryTerm.objects.all().order_by('term')
    return _page(request, 'agency/glossary.html', {'terms': terms})


def contacts_view(request):
    info = CompanyInfo.objects.filter(section=CompanyInfo.SECTION_CONTACTS)
    employees = Employee.objects.select_related('user').all()
    weather = get_weather()
    return _page(request, 'agency/contacts.html', {
        'info': info,
        'employees': employees,
        'weather': weather,
    })


def privacy_view(request):
    sections = CompanyInfo.objects.filter(section=CompanyInfo.SECTION_PRIVACY)
    return _page(request, 'agency/privacy.html', {'sections': sections})


def vacancies_view(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return _page(request, 'agency/vacancies.html', {'vacancies': vacancies})


def reviews_view(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                role = get_user_role(request.user)
                if role == ROLE_CLIENT and hasattr(request.user, 'buyer_profile'):
                    review.name = request.user.buyer_profile.full_name
                else:
                    review.name = (
                        request.user.get_full_name() or request.user.username
                    )
                review.is_published = False
                review.save()
                messages.success(request, 'Отзыв отправлен на модерацию.')
                return redirect('agency:reviews')
        else:
            form = ReviewForm()
    return _page(request, 'agency/reviews.html', {
        'reviews': reviews,
        'form': form,
    })


def promocodes_view(request):
    today = timezone.now().date()
    active = PromoCode.objects.filter(is_active=True, valid_until__gte=today)
    archive = PromoCode.objects.filter(
        Q(is_active=False) | Q(valid_until__lt=today),
    )
    return _page(request, 'agency/promocodes.html', {
        'active_codes': active,
        'archive_codes': archive,
    })


@admin_required
def statistics_view(request):
    """Statistics and matplotlib charts (admin only)."""
    stats = compute_statistics()
    charts = generate_all_charts()
    return _page(request, 'agency/statistics.html', {
        'stats': stats,
        'charts': charts,
    })


@require_POST
def set_timezone_view(request):
    """Save timezone to session and user profile."""
    tz_name = request.POST.get('timezone', '').strip()
    if not is_valid_timezone(tz_name):
        messages.error(request, 'Некорректная таймзона.')
    else:
        request.session['user_timezone'] = tz_name
        if request.user.is_authenticated:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.timezone = tz_name
            profile.save(update_fields=['timezone'])
        messages.success(request, f'Часовой пояс: {tz_name}')
    return redirect(request.POST.get('next', 'agency:home'))


@login_required_api
def api_weather_view(request):
    """Weather JSON API (authenticated users only)."""
    city = request.GET.get('city')
    data = get_weather(city)
    return JsonResponse(data)


@login_required_api
def api_exchange_rates_view(request):
    """Exchange rates JSON API (authenticated users only)."""
    return JsonResponse(get_exchange_rates())


# --- Real estate ---


def property_list_view(request):
    queryset = RealEstate.objects.select_related(
        'property_type', 'owner',
    ).all()
    queryset, filters = filter_properties(queryset, request.GET)
    property_types = PropertyType.objects.all()
    rates = get_exchange_rates()
    user_zone = get_user_timezone(request)
    properties_with_dates = []
    for prop in queryset:
        properties_with_dates.append({
            'obj': prop,
            'created_utc': format_datetime_ddmmyyyy(prop.created_at, None),
            'created_local': format_datetime_ddmmyyyy(prop.created_at, user_zone),
        })
    return _page(request, 'agency/property_list.html', {
        'properties': queryset,
        'properties_with_dates': properties_with_dates,
        'property_types': property_types,
        'filters': filters,
        'status_choices': RealEstate.STATUS_CHOICES,
        'exchange_rates': rates,
    })


def property_detail_view(request, pk):
    prop = get_object_or_404(
        RealEstate.objects.select_related('property_type', 'owner'),
        pk=pk,
    )
    user_zone = get_user_timezone(request)
    rates = get_exchange_rates()
    geo = geocode_address(prop.address)
    price_usd = None
    price_eur = None
    if rates.get('USD_per_byn') and prop.price:
        price_usd = round(float(prop.price) * float(rates['USD_per_byn']), 2)
    if rates.get('EUR_per_byn') and prop.price:
        price_eur = round(float(prop.price) * float(rates['EUR_per_byn']), 2)
    return _page(request, 'agency/property_detail.html', {
        'property': prop,
        'created_at_utc': format_datetime_ddmmyyyy(prop.created_at, None),
        'created_at_local': format_datetime_ddmmyyyy(prop.created_at, user_zone),
        'updated_at_utc': format_datetime_ddmmyyyy(prop.updated_at, None),
        'updated_at_local': format_datetime_ddmmyyyy(prop.updated_at, user_zone),
        'exchange_rates': rates,
        'price_usd': price_usd,
        'price_eur': price_eur,
        'geo': geo,
    })


def property_create_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Недостаточно прав.')
        return redirect('agency:property_list')
    if request.method == 'POST':
        form = RealEstateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            logger.info(
                'Property %s created by %s',
                obj.pk,
                request.user.username,
            )
            messages.success(request, 'Объект создан.')
            return redirect('agency:property_list')
        logger.error('Property creation failed: %s', form.errors)
    else:
        form = RealEstateForm()
    return _page(request, 'agency/property_form.html', {
        'form': form,
        'title': 'Добавить объект',
    })


def property_update_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Недостаточно прав.')
        return redirect('agency:property_list')
    prop = get_object_or_404(RealEstate, pk=pk)
    if request.method == 'POST':
        form = RealEstateForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            logger.info(
                'Property %s updated by %s',
                pk,
                request.user.username,
            )
            messages.success(request, 'Объект обновлён.')
            return redirect('agency:property_detail', pk=pk)
        logger.error('Property update failed: %s', form.errors)
    else:
        form = RealEstateForm(instance=prop)
    return _page(request, 'agency/property_form.html', {
        'form': form,
        'title': 'Редактировать объект',
        'property': prop,
    })


def property_delete_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Недостаточно прав.')
        return redirect('agency:property_list')
    prop = get_object_or_404(RealEstate, pk=pk)
    if request.method == 'POST':
        prop_id = prop.pk
        prop.delete()
        logger.info(
            'Property %s deleted by %s',
            prop_id,
            request.user.username,
        )
        messages.success(request, 'Объект удалён.')
        return redirect('agency:property_list')
    return _page(request, 'agency/property_confirm_delete.html', {'property': prop})


# --- Deals ---


def _deals_for_user(user):
    role = get_user_role(user)
    if role == ROLE_ADMIN:
        return Deal.objects.all()
    if role == ROLE_EMPLOYEE:
        return Deal.objects.filter(employee=user.employee_profile)
    if role == ROLE_CLIENT:
        buyer = get_client_buyer(user)
        if buyer:
            return Deal.objects.filter(buyer=buyer)
    return Deal.objects.none()


@login_required
def deal_list_view(request):
    deals = _deals_for_user(request.user).select_related(
        'real_estate', 'employee', 'buyer',
    ).order_by('-deal_date')
    return _page(request, 'agency/deal_list.html', {'deals': deals})


@client_required
def my_deals_view(request):
    return deal_list_view(request)


@client_required
def my_purchases_view(request):
    return deal_list_view(request)


@client_required
def create_deal_view(request):
    buyer = get_client_buyer(request.user)
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            estate = form.cleaned_data['real_estate']
            employee = Employee.objects.first()
            if not employee:
                logger.error('Deal creation failed: no employees available')
                messages.error(request, 'Нет доступных сотрудников.')
            else:
                deal = Deal.objects.create(
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
                logger.info(
                    'Deal %s created by user %s',
                    deal.pk,
                    request.user.username,
                )
                messages.success(request, 'Сделка оформлена.')
                return redirect('agency:my_purchases')
        logger.error('Deal creation failed: %s', form.errors)
    else:
        form = DealForm()
    return _page(request, 'agency/deal_form.html', {
        'form': form,
        'title': 'Оформить сделку',
    })


def _can_edit_deal(user, deal):
    role = get_user_role(user)
    if role == ROLE_ADMIN:
        return True
    if role == ROLE_EMPLOYEE:
        return deal.employee_id == user.employee_profile.id
    return False


@login_required
def deal_update_view(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if not _can_edit_deal(request.user, deal):
        messages.error(request, 'Недостаточно прав.')
        return redirect('agency:deal_list')
    employee_only = get_user_role(request.user) == ROLE_EMPLOYEE
    if request.method == 'POST':
        form = DealManageForm(
            request.POST,
            instance=deal,
            employee_only=employee_only,
        )
        if form.is_valid():
            updated = form.save(commit=False)
            if employee_only:
                updated.employee = request.user.employee_profile
            updated.save()
            messages.success(request, 'Сделка обновлена.')
            return redirect('agency:deal_list')
    else:
        form = DealManageForm(instance=deal, employee_only=employee_only)
    return _page(request, 'agency/deal_form.html', {
        'form': form,
        'title': 'Редактировать сделку',
        'deal': deal,
    })


@admin_required
def deal_create_admin_view(request):
    if request.method == 'POST':
        form = DealAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сделка создана.')
            return redirect('agency:deal_list')
    else:
        form = DealAdminForm()
    return _page(request, 'agency/deal_form.html', {
        'form': form,
        'title': 'Новая сделка (админ)',
    })


@admin_required
def deal_delete_view(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, 'Сделка удалена.')
        return redirect('agency:deal_list')
    return _page(request, 'agency/deal_confirm_delete.html', {'deal': deal})


@login_required
def add_review_view(request):
    return redirect('agency:reviews')


@employee_required
def employee_dashboard_view(request):
    employee = request.user.employee_profile
    deals = Deal.objects.filter(employee=employee).select_related(
        'real_estate', 'buyer',
    )
    estate_ids = deals.values_list('real_estate_id', flat=True).distinct()
    buyer_ids = deals.values_list('buyer_id', flat=True).distinct()
    return _page(request, 'agency/employee_dashboard.html', {
        'deals': deals,
        'estates': RealEstate.objects.filter(id__in=estate_ids),
        'buyers': Buyer.objects.filter(id__in=buyer_ids),
    })
