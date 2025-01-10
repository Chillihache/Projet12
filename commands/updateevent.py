import click
from datetime import datetime
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.check_date import prompt_for_date
from eventhub.models import Event, Contract
from django.contrib.auth.models import Group



@click.command()
@click.argument("name")
def updateevent(name):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.change_event'):
            click.secho("Vous n'avez pas la permission de modifier un événement.", fg="red")
            return

        event = Event.objects.filter(name=name).first()

        if not event:
            click.secho("Cet évennement n'existe pas.", fg="red")
            return

        if user.groups.filter(name="Support") and user != event.support_contact:
            click.secho("Vous n'êtes pas en charge de cet événement.", fg="red")
            return

        if user.groups.filter(name="Management"):
            supports = Group.objects.get(name='Support').user_set.all()
            if len(supports) == 0:
                click.secho("Aucun collaborateur dans le département support.", fg="red")
                return
            else:
                supports = list(supports)
                click.secho("Veuillez choisir un colaborateur du département support a affecter à l'événement :", fg="red")

                for i, support in enumerate(supports, start=1):
                    click.echo(f"{i}. {support.first_name} {support.last_name}")

                click.secho(f"{len(supports) + 1}. Ne pas assigner de support", fg="yellow")

                support_choice = None
                while support_choice not in range(1, len(supports) + 2):
                    try:
                        support_choice = int(click.prompt("Votre choix", type=int))
                        if support_choice not in range(1, len(supports) + 2):
                            click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
                    except ValueError:
                        click.secho("Entrée invalide.", fg="red")

                if support_choice == len(supports) + 1:
                    support_contact = None
                else:
                    support_contact = supports[support_choice - 1]

                event.support_contact = support_contact
                event.save()
                click.secho("Contact support modifié avec succès !", fg="green")

        else:
            click.echo(f"Modification des informations de l'événement {event.name}.\n"
                       "Laissez vides les champs que vous ne souhaitez pas modifier.")

            new_name = None
            while not new_name:
                new_name = click.prompt("Nouveau nom", default=event.name)
                if Event.objects.filter(name=new_name).exists():
                    if new_name != event.name:
                        click.secho("Ce nom d'évennement existe déjà.", fg="red")
                        new_name = None

            modify_date_choice = click.confirm("Souhaitez-vous modifier les dates de début et de fin ?")

            if modify_date_choice:
                new_event_date_start = prompt_for_date("Date de début (format: YYYY-MM-DD HH:MM)")
                new_event_date_end = prompt_for_date("Date de fin (format: YYYY-MM-DD HH:MM)")
            else:
                new_event_date_start = event.event_date_start
                new_event_date_end = event.event_date_end

            new_location = click.prompt("Nouvelle adresse", default=event.location)

            while True:
                try:
                    new_attendees = int(click.prompt("Nouveau nombre d'invités", default=event.attendees))
                    if new_attendees >= 1:
                        break
                    else:
                        click.secho("Le nombre d'invités doit être égal ou supérieur à 1.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez entrer un nombre entier.", fg="red")

            new_notes = click.prompt("Nouvelles informations supplémentaires", default=event.notes)

            event.name = new_name
            event.event_date_start = new_event_date_start
            event.event_date_end = new_event_date_end
            event.location = new_location
            event.attendees = new_attendees
            event.notes = new_notes

            event.save()

            click.secho("L'Evénement a été modifié avec succès !", fg="green")




