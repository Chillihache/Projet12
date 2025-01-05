import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Client


@click.command()
def getclients():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_client'):
            click.echo("Vous n'avez pas la permission de voir les clients")
            return
    clients = Client.objects.all()
    click.echo(clients)
