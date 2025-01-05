import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Event


@click.command()
def getevents():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_event'):
            click.echo("Vous n'avez pas la permission de voir les évennements")
            return
        events = Event.objects.all()
        click.echo(events)