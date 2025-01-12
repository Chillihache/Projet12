import click
from rich.console import Console
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.create_table import create_clients_table
from eventhub.models import Client


@click.command()
def getclients():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_client'):
            click.secho("Vous n'avez pas la permission de voir les clients.", fg="red")
            return

        clients = Client.objects.all()
        console = Console()
        table = create_clients_table(clients)

        console.print(table)


