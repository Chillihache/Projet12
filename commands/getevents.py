import click
from rich.console import Console
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.create_table import create_events_table
from eventhub.models import Event


@click.command()
def getevents():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_event'):
            click.secho("Vous n'avez pas la permission de voir les événements.", fg="red")
            return

        events = Event.objects.all()
        console = Console()
        table = create_events_table(events)

        console.print(table)