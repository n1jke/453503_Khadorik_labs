"""Signals: user profile, groups, employee role sync."""

from django.contrib.auth.models import Group, User
from django.db import connection
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Employee, UserProfile

GROUP_CLIENTS = 'Clients'
GROUP_EMPLOYEES = 'Employees'


def ensure_role_groups():
    """Create Clients and Employees groups (after auth tables exist)."""
    if 'auth_group' not in connection.introspection.table_names():
        return
    Group.objects.get_or_create(name=GROUP_CLIENTS)
    Group.objects.get_or_create(name=GROUP_EMPLOYEES)


@receiver(post_migrate)
def setup_role_groups_after_migrate(sender, **kwargs):
    """Run after migrations so migrate/entrypoint does not hit missing tables."""
    if sender.name != 'agency':
        return
    ensure_role_groups()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create client profile for new users (except superuser)."""
    if created and not instance.is_superuser:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': UserProfile.ROLE_CLIENT},
        )


@receiver(post_save, sender=Employee)
def sync_employee_role(sender, instance, **kwargs):
    """On employee create: set employee role and add to Employees group."""
    profile, _ = UserProfile.objects.get_or_create(user=instance.user)
    if profile.role != UserProfile.ROLE_EMPLOYEE:
        profile.role = UserProfile.ROLE_EMPLOYEE
        profile.save(update_fields=['role'])
    group = Group.objects.filter(name=GROUP_EMPLOYEES).first()
    if group:
        instance.user.groups.add(group)
