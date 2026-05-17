"""Сигналы: профиль пользователя, группы, синхронизация роли сотрудника."""

from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Employee, UserProfile

GROUP_CLIENTS = 'Clients'
GROUP_EMPLOYEES = 'Employees'


def ensure_role_groups():
    """Создать группы Clients и Employees при старте приложения."""
    Group.objects.get_or_create(name=GROUP_CLIENTS)
    Group.objects.get_or_create(name=GROUP_EMPLOYEES)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Профиль с ролью client для новых пользователей (кроме суперюзера)."""
    if created and not instance.is_superuser:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': UserProfile.ROLE_CLIENT},
        )


@receiver(post_save, sender=Employee)
def sync_employee_role(sender, instance, **kwargs):
    """При создании сотрудника — роль employee в профиле и группа Employees."""
    profile, _ = UserProfile.objects.get_or_create(user=instance.user)
    if profile.role != UserProfile.ROLE_EMPLOYEE:
        profile.role = UserProfile.ROLE_EMPLOYEE
        profile.save(update_fields=['role'])
    group = Group.objects.filter(name=GROUP_EMPLOYEES).first()
    if group:
        instance.user.groups.add(group)
