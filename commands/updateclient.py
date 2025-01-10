import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import Client


@click.command()
@click.argument("email")
def updateclient(email):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.change_client'):
            click.secho("Vous n'avez pas la permission de modifier un client.", fg="red")
            return

        client = Client.objects.filter(email=email).first()

        if not client:
            click.secho("Le client n'existe pas.", fg="red")
            return

        if user != client.sales_contact:
            click.secho("Vous n'êtes pas en charge de ce client.", fg="red")
            return

        click.echo(f"Modification des informations du client {client.first_name} {client.last_name}.\n"
                   f"Laissez vides les champs que vous ne souhaitez pas modifier")

        new_first_name = click.prompt("Nouveau prénom", default=client.first_name)
        new_last_name = click.prompt("Nouveau nom de famille", default=client.last_name)

        new_email = None
        while not new_email:
            new_email = click.prompt("Nouvel email", default=client.email)
            if Client.objects.filter(email=new_email).exists():
                if new_email != client.email:
                    click.secho("Cette email est déjà utilisé par un client.", fg="red")
                    new_email = None
        new_company_name = click.prompt("Nouveau nom d'entrepirse", default=client.company_name)

        client.first_name = new_first_name
        client.last_name = new_last_name
        client.email = new_email
        client.company_name = new_company_name

        client.save()

        click.secho("Le client a été modifé avec succès !", fg="green")