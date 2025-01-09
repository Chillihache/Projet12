import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Contract, Client, CustomUser


@click.command()
def createcontract():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_contract'):
            click.echo("Vous n'avez pas la permission de créer un contrat.")
            return

        click.echo("Veuillez renseigner les champs suivants pour la création du contrat :")
        contract_number = click.prompt("Numéro de contrat")
        contract_number.upper()

        if Contract.objects.filter(contract_number=contract_number).exists():
            click.echo("Un contrat avec ce numéro existe déjà")
            return

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

        client = clients[client_choice - 1]

        total_amount = None
        while not total_amount:
            try:
                total_amount = click.prompt("Montant total")
                total_amount = float(total_amount)
                if len(str(total_amount).split(".")[1]) > 2:
                    click.echo("Le montant doit comporter maximum deux chiffres après la virgule.")
                    total_amount = None
            except ValueError:
                click.echo("Montant incorrect")
                total_amount = None

        remaining_amount = None
        while not remaining_amount:
            try:
                remaining_amount = click.prompt("Montant restant")
                remaining_amount = float(remaining_amount)
                if len(str(remaining_amount).split(".")[1]) > 2:
                    click.echo("Le montant doit comporter maximum deux chiffres après la virgule.")
                    remaining_amount = None
            except ValueError:
                click.echo("Montant incorrect")
                remaining_amount = None


        is_signed = click.confirm("Le contrat est-il signé ?", default=False)

        contract = Contract(
            contract_number=contract_number,
            client=client,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed
        )

        contract.save()

        click.echo("Le contrat a été créé avec succès")


