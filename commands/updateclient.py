import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Client


@click.command()
@click.argument("email")
def updateclient(email):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.change_client'):
            click.echo("Vous n'avez pas la permission de modifier un contrat.")
            return

        client = Client.objects.filter(email=email).first()

        if not client:
            click.echo("Le client n'existe pas.")
            return

        if user != client.sales_contact:
            click.echo("Vous n'êtes pas en charge de ce client.")
            return

        click.echo(f"Modification des informations du client {client.first_name} {client.last_name} "
                   f"Laissez vides les champs que vous ne souhaitez pas modifier")

        new_first_name = click.prompt("Nouveau prénom", default=client.first_name)
        new_last_name = click.prompt("Nouveau nom de famille", default=client.last_name)

        new_email = None
        while not new_email:
            new_email = click.prompt("Nouvel email", default=client.email)
            if Client.objects.filter(email=new_email).exists():
                if new_email != client.email:
                    click.echo("Cette email est déjà utilisé par un client")
                    new_email = None
        new_company_name = click.prompt("Nouveau nom d'entrepirse", default=client.company_name)

        client.first_name = new_first_name
        client.last_name = new_last_name
        client.email = new_email
        client.company_name = new_company_name

        client.save()

        click.echo("Le client a été modifé avec succès !")