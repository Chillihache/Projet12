import os
import django
import click


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

from commands.hello import hello
from commands.creategroups import creategroups
from commands.login import login
from commands.createuser import createuser
from commands.getclients import getclients
from commands.getcontracts import getcontracts
from commands.getevents import getevents

@click.group()
def cli():
    pass

cli.add_command(hello)
cli.add_command(creategroups)
cli.add_command(login)
cli.add_command(createuser)
cli.add_command(getclients)
cli.add_command(getcontracts)
cli.add_command(getevents)

if __name__ == "__main__":
    cli()
