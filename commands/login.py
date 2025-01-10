import click
import requests
from eventhub.utils.jwt_tokens import save_tokens, generate_jwt
from eventhub.models import CustomUser

@click.command()
def login():

        click.echo("Veuillez entrer les informations suivantes :")
        email = click.prompt("Email")

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            click.secho("Utilisateur inconnu.", fg="red")
            return

        password = click.prompt("Mot de passe", hide_input=True)

        if user.check_password(password):
            access_token, refresh_token = generate_jwt(email, password)

            save_tokens(access_token, refresh_token)

            click.secho("Connexion réussie et tokens générés !", fg="green")

        else:
            click.secho("Mot de passe incorrect.", fg="red")


