import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import CustomUser
from django.contrib.auth.models import Group


@click.command()
def createuser():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_customuser'):
            click.echo("Vous n'avez pas la permission de créer un utilisateur")
            return

        try:
            groups = Group.objects.values_list("name", flat=True)

            if not groups:
                click.echo("Veuillez configurez les groupes avec la commande : python cli.py creategroups")
                return

            click.echo("Veuillez renseigner les informaitons suivantes :")
            email = click.prompt("Email")
            if CustomUser.objects.filter(email=email).exists():
                click.echo(f"Un utilisateur avec l'email {email} existe déjà.")
                return

            password = click.prompt("Mot de passe",
                                    hide_input=True,
                                    confirmation_prompt="Veuillez répéter le mot de passe pour confirmation")

            employee_number = click.prompt("Numéro d'employé")

            if CustomUser.objects.filter(employee_number=employee_number).exists():
                click.echo(f"Un utilisateur avec le numéro d'employé {employee_number} existe déjà.")
                return

            first_name = click.prompt("Prénom")
            last_name = click.prompt("Nom")

            click.echo("Veuillez choisir un département :")
            groups = list(groups)
            for i, group_name in enumerate(groups, start=1):
                click.echo(f"{i}. {group_name}")

            group_choice = None
            while group_choice not in range(1, len(groups) + 1):
                try:
                    group_choice = int(click.prompt("Entrez le numéro du groupe", type=int))
                    if group_choice not in range(1, len(groups) + 1):
                        click.echo("Choix invalide. Veuillez sélectionner un numéro valide.")
                except ValueError:
                    click.echo("Entrée invalide. Veuillez choisir un département.")

            group_name = groups[group_choice - 1]
            group = Group.objects.get(name=group_name)

            user = CustomUser(
                email=email,
                employee_number=employee_number,
                first_name=first_name,
                last_name=last_name
            )
            # Hacher le mot de passe
            user.set_password(password)
            user.save()
            user.groups.add(group)

            click.echo(f"Utilisateur {email} créé avec succès.")

        except Exception as e:
            click.echo(f"Erreur lors de la création de l'utilisateur : {e}")


