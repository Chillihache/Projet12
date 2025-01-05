import click
from django.contrib.auth.models import Group, Permission
import django


@click.command()
def creategroups():
    groups_permissions = {
        "Sales": ["view_client", "view_contract", "view_event",
                  "add_client", "change_client",
                  "change_contract", "filter_contracts",
                  "add_event"],
        "Support": ["view_client", "view_contract", "view_event",
                    "add_customuser", "change_customuser", "delete_customuser", "view_customuser",
                    "add_contract", "change_contract",
                    "change_event", "filter_events"],
        "Management": ["view_client", "view_contract", "view_event",
                       "change_event_support_contact", "filter_events"],
    }

    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            click.secho(f"{group_name} group created", fg="green", bold=True)
        else:
            click.secho(f"{group_name} group already exists", fg="yellow")

        for codename in permissions:
            permission = Permission.objects.none
            try:
                permission = Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                click.secho(f"  - Permission '{codename}' not found", fg="red", bold=True)

            group.permissions.add(permission)
            click.secho(f"  - Permission '{codename}' added to group '{group_name}'", fg="cyan")

    click.secho("Groups and permissions successfully configured", fg="green", bold=True)

