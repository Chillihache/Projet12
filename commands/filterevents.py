import click
from rich.console import Console
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.create_table import create_events_table
from eventhub.models import Event


@click.command()
def filterevents():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.filter_events'):
            click.secho("Vous n'avez pas la permission de filter les événements.", fg="red")
            return

        console = Console()

        if user.groups.filter(name="Support").exists():
            events = Event.objects.filter(support_contact=user)

        elif user.groups.filter(name="Management").exists():
            events = Event.objects.filter(support_contact=None)

        else:
            click.secho("Vous n'êtes ni dans le département gestion ni dans le département support, "
                       "vous ne pouvez pas filtrer les événements.", fg="red")
            return

        table = create_events_table(events)

        console.print(table)