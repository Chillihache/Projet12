import click
from rich.console import Console
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.create_table import create_contracts_table
from eventhub.models import Contract


@click.command()
def getcontracts():
    user = authenticate_user()
    if user:
        if not user.is_superuser and not user.has_perm('eventhub.view_contract'):
            click.secho("Vous n'avez pas la permission de voir les contrats.", fg="red")
            return

        contracts = Contract.objects.all()
        console = Console()
        table = create_contracts_table(contracts)

        console.print(table)