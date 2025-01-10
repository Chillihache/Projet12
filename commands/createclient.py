import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Client


@click.command()
def createclient():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_client'):
            click.secho("Vous n'avez pas la permission de créer un client.", fg="red")
            return

        if user.groups.filter(name="Sales").exists():

            click.echo("Veuillez renseigner les champs suivants pour la création du client :")

            first_name = click.prompt("Prénom")
            last_name = click.prompt("Nom de famille")

            email=None
            while not email:
                email = click.prompt("Email")
                if Client.objects.filter(email=email).exists():
                    click.secho("Cette email est déjà utilisé par un client.", fg="red")
                    email = None

            company_name = click.prompt("Nom de l'entrepise")

            client = Client(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            company_name=company_name,
                            sales_contact=user)

            client.save()

            click.secho("Le client a été créé avec succès !", fg="green")

        else:
            click.secho("Vous n'êtes pas dans le département commercial, vous ne pouvez pas créer un client.", fg="red")