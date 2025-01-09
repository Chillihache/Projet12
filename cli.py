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
from commands.deleteuser import deleteuser
from commands.updateuser import updateuser
from commands.createcontract import createcontract
from commands.updatecontract import updatecontract
from commands.filterevents import filterevents
from commands.createclient import createclient
from commands.updateclient import updateclient
from commands.filtercontracts import filtercontracts
from commands.createevent import createevent
from commands.updateevent import updateevent

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
cli.add_command(deleteuser)
cli.add_command(updateuser)
cli.add_command(createcontract)
cli.add_command(updatecontract)
cli.add_command(filterevents)
cli.add_command(createclient)
cli.add_command(updateclient)
cli.add_command(filtercontracts)
cli.add_command(createevent)
cli.add_command(updateevent)

if __name__ == "__main__":
    cli()
