"""Sync UserProfile and groups for existing users."""

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from agency.models import Employee, UserProfile
from agency.signals import GROUP_CLIENTS, GROUP_EMPLOYEES, ensure_role_groups


class Command(BaseCommand):
    help = 'Создаёт профили и группы для уже существующих пользователей.'

    def handle(self, *args, **options):
        ensure_role_groups()
        clients_group = Group.objects.get(name=GROUP_CLIENTS)
        employees_group = Group.objects.get(name=GROUP_EMPLOYEES)

        for user in User.objects.all():
            if user.is_superuser:
                continue
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if hasattr(user, 'employee_profile'):
                profile.role = UserProfile.ROLE_EMPLOYEE
                profile.save(update_fields=['role'])
                user.groups.add(employees_group)
            else:
                profile.role = UserProfile.ROLE_CLIENT
                profile.save(update_fields=['role'])
                user.groups.add(clients_group)

        self.stdout.write(self.style.SUCCESS('Профили синхронизированы.'))
