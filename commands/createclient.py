import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Client


@click.command()
def createclient():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_client'):
            click.echo("Vous n'avez pas la permission de créer un client.")
            return

        if user.groups.filter(name="Sales").exists():

            click.echo("Veuillez renseigner les champs suivants pour la création du client :")

            first_name = click.prompt("Prénom")
            last_name = click.prompt("Nom de famille")

            email=None
            while not email:
                email = click.prompt("Email")
                if Client.objects.filter(email=email).exists():
                    click.echo("Cette email est déjà utilisé par un client.")
                    email = None

            company_name = click.prompt("Nom de l'entrepise")

            client = Client(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            company_name=company_name,
                            sales_contact=user)

            client.save()

            click.echo("Le client a été créé avec succès !")

        else:
            click.echo("Vous n'êtes pas dans le département commercial")