from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        groups_permissions = {
            "Sales": ["view_client", "view_contract", "view_event",
                      "add_client", "change_client",
                      "change_contract", "filter_contracts",
                      "add_event"],
            "Support": ["view_client", "view_contract", "view_event",
                        "add_user", "change_user", "delete_user", "view_user",
                        "add_contract", "change_contract",
                        "change_event", "filter_events"],
            "Management": ["view_client", "view_contract", "view_event",
                           "change_event_support_contact", "filter_events"],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"{group_name} group created"))
            else:
                self.stdout.write(f"{group_name} group already exists")

            for codename in permissions:
                try:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)
                    self.stdout.write(f"  - Permission '{codename}' added to group '{group_name}'")
                except Permission.DoesNotExist:
                    self.stderr.write(f"  - Permission '{codename}' not found")

        self.stdout.write(self.style.SUCCESS("Groups and permissions successfully configured"))
