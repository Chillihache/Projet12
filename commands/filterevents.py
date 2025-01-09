import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Event


@click.command()
def filterevents():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.filter_events'):
            click.echo("Vous n'avez pas la permission de filter les évennements")
            return

        if user.groups.filter(name="Support").exists():
            events = Event.objects.filter(support_contact=user)

        elif user.groups.filter(name="Management").exists():
            events = Event.objects.filter(support_contact=None)

        else:
            click.echo("Vous n'êtes ni dans le département gestion ni dans le département support.")
            return

        click.echo(events)