"""URL-маршруты приложения agency (re_path)."""

from django.urls import re_path

from . import views

app_name = 'agency'

urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^register/?$', views.register_view, name='register'),
    re_path(r'^login/?$', views.login_view, name='login'),
    re_path(r'^logout/?$', views.logout_view, name='logout'),
    re_path(r'^my-deals/?$', views.my_deals_view, name='my_deals'),
    re_path(r'^deals/create/?$', views.create_deal_view, name='create_deal'),
    re_path(r'^reviews/add/?$', views.add_review_view, name='add_review'),
    re_path(
        r'^employee/dashboard/?$',
        views.employee_dashboard_view,
        name='employee_dashboard',
    ),
    re_path(
        r'^admin-panel/?$',
        views.admin_dashboard_view,
        name='admin_dashboard',
    ),
]
