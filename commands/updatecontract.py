import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Contract, Client


@click.command()
@click.argument("contract_number")
def updatecontract(contract_number):

    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.change_contract'):
            click.echo("Vous n'avez pas la permission de modifier un contrat.")
            return

        contract_number.upper()
        contract = Contract.objects.filter(contract_number=contract_number).first()

        if not contract:
            click.echo("Ce contrat n'existe pas.")
            return

        if user.groups.filter(name="Sales") and user != contract.client.sales_contact:
            click.echo("Vous n'êtes pas en charge de ce contrat")
            return

        click.echo(f"Modification des informations du contrat {contract_number}. "
                   f"Laissez vides les champs que vous ne souhaitez pas modifier")

        new_contract_number = None
        while not new_contract_number:
            new_contract_number = click.prompt("Nouveau numéro de contrat", default=contract.contract_number)
            new_contract_number.upper()
            if Contract.objects.filter(contract_number=new_contract_number).exists():
                if new_contract_number != contract.contract_number:
                    click.echo("Ce numéro de contrat existe déjà")
                    new_contract_number = None

        new_total_amount = None
        while not new_total_amount:
            try:
                new_total_amount = click.prompt("Nouveau montant total", default=contract.total_amount)
                new_total_amount = float(new_total_amount)
                if len(str(new_total_amount).split(".")[1]) > 2:
                    click.echo("Le montant doit comporter maximum deux chiffres après la virgule.")
                    new_total_amount = None
            except ValueError:
                click.echo("Montant incorrect")
                new_total_amount = None

        new_remaining_amount = None
        while not new_remaining_amount:
            try:
                new_remaining_amount = click.prompt("Nouveau montant restant", default=contract.remaining_amount)
                new_remaining_amount = float(new_remaining_amount)
                if len(str(new_remaining_amount).split(".")[1]) > 2:
                    click.echo("Le montant doit comporter maximum deux chiffres après la virgule.")
                    new_remaining_amount = None
            except ValueError:
                click.echo("Montant incorrect")
                new_remaining_amount = None

        new_is_signed = click.confirm("Le contrat est-il signé ?", default=contract.is_signed)

        client_choice = click.confirm(f"Le client lié au contrat est {contract.client}. Souhaitez-vous le modifier ?")

        if client_choice:
            clients = Client.objects.all()
            click.echo("Veuillez choisir un client :")
            clients_str = list(clients)
            for i, client_str in enumerate(clients_str, start=1):
                click.echo(f"{i}. {client_str}")

            client_choice = None

            while client_choice not in range(1, len(clients) + 1):
                try:
                    client_choice = int(click.prompt("Entrez le numéro du client", type=int))
                    if client_choice not in range(1, len(clients) + 1):
                        click.echo("Choix invalide. Veuillez sélectionner un numéro valide.")
                except ValueError:
                    click.echo("Entrée invalide. Veuillez choisir un client.")

            new_client = clients[client_choice - 1]

        else:
            new_client = contract.client

        contract.contract_number = new_contract_number
        contract.total_amount = new_total_amount
        contract.remaining_amount = new_remaining_amount
        contract.is_signed = new_is_signed
        contract.client = new_client

        contract.save()

        click.echo(f"Le contrat a été modifié avec succès !")




