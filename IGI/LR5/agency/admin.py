"""Регистрация моделей в админ-панели Django."""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
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
    Vacancy,
)


class RealEstateInline(admin.TabularInline):
    """Объекты недвижимости внутри вида."""

    model = RealEstate
    extra = 0
    fields = ('code', 'title', 'address', 'price', 'status')
    show_change_link = True


class DealInline(admin.TabularInline):
    """Сделки сотрудника."""

    model = Deal
    extra = 0
    fields = ('deal_type', 'real_estate', 'buyer', 'deal_date', 'amount')
    show_change_link = True
    autocomplete_fields = ('real_estate', 'buyer')


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_preview')
    search_fields = ('name', 'description')
    inlines = [RealEstateInline]

    @admin.display(description='Описание')
    def description_preview(self, obj):
        return obj.description[:80] + '…' if len(obj.description) > 80 else obj.description


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('created_at',)


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'address',
        'property_type',
        'price',
        'status',
        'photo_preview',
    )
    list_filter = ('status', 'property_type', 'created_at')
    search_fields = ('code', 'title', 'address', 'description')
    autocomplete_fields = ('owner', 'property_type')
    filter_horizontal = ('additional_types',)
    readonly_fields = ('photo_preview_large', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'code', 'title', 'address', 'property_type',
                'additional_types', 'owner', 'status',
            ),
        }),
        ('Характеристики', {
            'fields': ('area', 'price', 'rooms', 'floor', 'description'),
        }),
        ('Медиа', {
            'fields': ('photo', 'photo_preview_large'),
        }),
        ('Служебные', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;" />',
                obj.photo.url,
            )
        return '—'

    @admin.display(description='Превью фото')
    def photo_preview_large(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" style="max-height:200px;" />',
                obj.photo.url,
            )
        return 'Нет фото'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'position',
        'phone',
        'hired_date',
        'photo_preview',
    )
    list_filter = ('department', 'hired_date')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'department',
        'position',
        'phone',
    )
    inlines = [DealInline]
    readonly_fields = ('photo_preview_large',)

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover;" />',
                obj.photo.url,
            )
        return '—'

    @admin.display(description='Превью')
    def photo_preview_large(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="120" />',
                obj.photo.url,
            )
        return 'Нет фото'


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'birth_date', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('created_at',)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        'deal_type',
        'real_estate',
        'employee',
        'buyer',
        'deal_date',
        'amount',
        'created_at',
    )
    list_filter = ('deal_type', 'deal_date', 'created_at')
    search_fields = (
        'real_estate__code',
        'real_estate__title',
        'buyer__full_name',
        'employee__user__username',
    )
    autocomplete_fields = ('real_estate', 'employee', 'buyer')
    date_hierarchy = 'deal_date'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content', 'short_content')
    date_hierarchy = 'published_at'


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('section', 'title', 'updated_at')
    list_filter = ('section', 'updated_at')
    search_fields = ('title', 'content')


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'created_at')
    search_fields = ('term', 'definition')
    list_filter = ('created_at',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'created_at')
    search_fields = ('name', 'text')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'description')
