import click
import requests
from eventhub.utils.jwt_tokens import save_tokens, generate_jwt
from eventhub.models import CustomUser

@click.command()
@click.argument("email")
@click.argument("password")
def login(email, password):
    try:
        user = CustomUser.objects.get(email=email)

        if user.check_password(password):
            access_token, refresh_token = generate_jwt(email, password)

            save_tokens(access_token, refresh_token)

            click.echo(click.style('Connexion réussie et tokens générés !', fg='green'))

        else:
            click.echo("Mot de passe incorrect")

    except CustomUser.DoesNotExist:

        click.echo("Cette email n'est pas reconnu")
