import click
from datetime import datetime
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.utils.check_date import prompt_for_date
from django.contrib.auth.models import Group
from eventhub.models import Event, Contract, CustomUser



@click.command()
def createevent():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_event'):
            click.secho("Vous n'avez pas la permission de créer un événement.", fg="red")
            return

        click.echo("Veuillez renseigner les champs suivants pour la création de l'événement :")

        name = click.prompt("Nom")

        if Event.objects.filter(name=name).exists():
            click.secho("Il existe déjà un événement avec ce nom.", fg="red")
            return

        contracts = Contract.objects.filter(is_signed=True, client__sales_contact=user)

        if len(contracts) == 0:
            click.secho("Aucun contrat disponibles. (non signés)", fg="red")
            return

        click.echo("Veuillez choisir un contrat (contrats signés) :")
        contrats_str = list(contracts)
        for i, contrats_str in enumerate(contrats_str, start=1):
            click.echo(f"{i}. {contrats_str}")

        contract_choice = None

        while contract_choice not in range(1, len(contracts) + 1):
            try:
                contract_choice = int(click.prompt("Entrez le numéro du contrat", type=int))
                if contract_choice not in range(1, len(contracts) + 1):
                    click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
            except ValueError:
                click.secho("Entrée invalide. Veuillez choisir un contrat.", fg="red")

        contract = contracts[contract_choice - 1]

        event_date_start = prompt_for_date("Date de début (format: YYYY-MM-DD HH:MM)")
        event_date_end = prompt_for_date("Date de fin (format: YYYY-MM-DD HH:MM)")

        group_support = Group.objects.get(name="Support")
        supports = CustomUser.objects.filter(groups=group_support)

        if len(supports) == 0:
            click.secho("Aucun collaborateur dans le département support. Le champ 'Contact Support' restera vide.", fg="yellow")
            support_contact = None
        else:
            supports = list(supports)
            click.echo("Veuillez choisir un colaborateur du département support a affecter à l'événement :")

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

            location = click.prompt("Adresse")

            while True:
                try:
                    attendees = int(click.prompt("Nombre d'invités"))
                    if attendees >= 1:
                        break
                    else:
                        click.secho("Le nombre d'invités doit être égal ou supérieur à 1.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez entrer un nombre entier.", fg="red")

            notes = click.prompt("Informations supplémentaires (Peut être laissé vide)", default="", show_default=False)

            event = Event(
                name=name,
                contract = contract,
                event_date_start=event_date_start,
                event_date_end=event_date_end,
                support_contact = support_contact,
                location=location,
                attendees=attendees,
                notes=notes
            )

            event.save()

            click.secho("Evénement créé avec succès !", fg="green")












