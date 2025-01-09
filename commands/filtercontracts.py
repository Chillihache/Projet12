import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Contract


@click.command()
def filtercontracts():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.filter_contract'):
            click.echo("Vous n'avez pas la permission de filtrer les contrats")
            return

        click.echo("Choisissez votre filtre :\n"
                   "1 - Contrats non signés \n"
                   "2 - Contrats non réglés \n")

        while True:
            filter_choice = click.prompt("Votre choix")

            try:
                filter_choice = int(filter_choice)
                if filter_choice in (1, 2):
                    break
            except ValueError:
                pass
            click.echo("Choix invalide.")

        if filter_choice == 1:
            contracts = Contract.objects.filter(is_signed=False)
        else:
            contracts = Contract.objects.filter(remaining_amount__gt=0)

        click.echo(contracts)

