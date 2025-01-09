import click
import requests
from eventhub.utils.jwt_tokens import save_tokens, generate_jwt
from eventhub.models import CustomUser

@click.command()
def login():

        click.echo("Veuillez entrer les informaitons suivantes :")
        email = click.prompt("Email")

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            click.echo("Cette email n'est pas reconnu")
            return

        password = click.prompt("Mot de passe", hide_input=True)

        if user.check_password(password):
            access_token, refresh_token = generate_jwt(email, password)

            save_tokens(access_token, refresh_token)

            click.echo(click.style('Connexion réussie et tokens générés !', fg='green'))

        else:
            click.echo("Mot de passe incorrect")


