import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Contract


@click.command()
def getcontracts():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_contract'):
            click.echo("Vous n'avez pas la permission de voir les contrats")
            return
        contracts = Contract.objects.all()
        click.echo(contracts)