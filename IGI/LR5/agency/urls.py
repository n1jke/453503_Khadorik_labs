"""URL-маршруты приложения agency (только re_path)."""

from django.urls import re_path

from . import views

app_name = 'agency'

urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^about/?$', views.about_view, name='about'),
    re_path(r'^news/?$', views.news_list_view, name='news_list'),
    re_path(r'^news/(?P<pk>\d+)/?$', views.news_detail_view, name='news_detail'),
    re_path(r'^glossary/?$', views.glossary_view, name='glossary'),
    re_path(r'^contacts/?$', views.contacts_view, name='contacts'),
    re_path(r'^privacy/?$', views.privacy_view, name='privacy'),
    re_path(r'^vacancies/?$', views.vacancies_view, name='vacancies'),
    re_path(r'^reviews/?$', views.reviews_view, name='reviews'),
    re_path(r'^reviews/add/?$', views.add_review_view, name='add_review'),
    re_path(r'^promocodes/?$', views.promocodes_view, name='promocodes'),
    re_path(r'^statistics/?$', views.statistics_view, name='statistics'),
    re_path(r'^timezone/set/?$', views.set_timezone_view, name='set_timezone'),
    re_path(r'^api/weather/?$', views.api_weather_view, name='api_weather'),
    re_path(
        r'^api/exchange-rates/?$',
        views.api_exchange_rates_view,
        name='api_exchange_rates',
    ),

    re_path(r'^properties/?$', views.property_list_view, name='property_list'),
    re_path(
        r'^properties/create/?$',
        views.property_create_view,
        name='property_create',
    ),
    re_path(
        r'^properties/(?P<pk>\d+)/edit/?$',
        views.property_update_view,
        name='property_update',
    ),
    re_path(
        r'^properties/(?P<pk>\d+)/delete/?$',
        views.property_delete_view,
        name='property_delete',
    ),
    re_path(
        r'^properties/(?P<pk>\d+)/?$',
        views.property_detail_view,
        name='property_detail',
    ),

    re_path(r'^register/?$', views.register_view, name='register'),
    re_path(r'^login/?$', views.login_view, name='login'),
    re_path(r'^logout/?$', views.logout_view, name='logout'),

    re_path(r'^deals/?$', views.deal_list_view, name='deal_list'),
    re_path(r'^deals/create/?$', views.create_deal_view, name='create_deal'),
    re_path(
        r'^deals/admin/create/?$',
        views.deal_create_admin_view,
        name='deal_create_admin',
    ),
    re_path(
        r'^deals/(?P<pk>\d+)/edit/?$',
        views.deal_update_view,
        name='deal_update',
    ),
    re_path(
        r'^deals/(?P<pk>\d+)/delete/?$',
        views.deal_delete_view,
        name='deal_delete',
    ),
    re_path(r'^my-deals/?$', views.my_deals_view, name='my_deals'),
    re_path(r'^my-purchases/?$', views.my_purchases_view, name='my_purchases'),
    re_path(
        r'^employee/dashboard/?$',
        views.employee_dashboard_view,
        name='employee_dashboard',
    ),
]
