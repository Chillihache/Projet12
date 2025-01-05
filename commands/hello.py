import click
from eventhub.utils.jwt_tokens import authenticate_user


@click.command()
def hello():
    user = authenticate_user()

    if user:
        click.echo(user)
        click.echo("Ceci est un test")
