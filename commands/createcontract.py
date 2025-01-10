import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Contract, Client, CustomUser


@click.command()
def createcontract():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_contract'):
            click.secho("Vous n'avez pas la permission de créer un contrat.", fg="red")
            return

        click.echo("Veuillez renseigner les champs suivants pour la création du contrat :")
        contract_number = click.prompt("Numéro de contrat")
        contract_number.upper()

        if Contract.objects.filter(contract_number=contract_number).exists():
            click.secho("Un contrat avec ce numéro existe déjà.", fg="red")
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
                    click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
            except ValueError:
                click.secho("Entrée invalide. Veuillez choisir un client.", fg="red")

        client = clients[client_choice - 1]

        total_amount = None
        while total_amount is None:
            try:
                total_amount = click.prompt("Montant total")
                total_amount = float(total_amount)
                if len(str(total_amount).split(".")[1]) > 2:
                    click.secho("Le montant doit comporter au maximum deux chiffres après la virgule.", fg="red")
                    total_amount = None
            except ValueError:
                click.secho("Montant incorrect", fg="red")
                total_amount = None

        remaining_amount = None
        while remaining_amount is None:
            try:
                remaining_amount = click.prompt("Montant restant")
                remaining_amount = float(remaining_amount)
                if len(str(remaining_amount).split(".")[1]) > 2:
                    click.secho("Le montant doit comporter maximum deux chiffres après la virgule.", fg="red")
                    remaining_amount = None
            except ValueError:
                click.secho("Montant incorrect", fg="red")
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

        click.secho("Le contrat a été créé avec succès !", fg="green")


