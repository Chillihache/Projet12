import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import CustomUser
from django.contrib.auth.models import Group


@click.command()
def createuser():
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.add_customuser'):
            click.secho("Vous n'avez pas la permission de créer un utilisateur.", fg="red")
            return

        try:
            groups = Group.objects.values_list("name", flat=True)

            if not groups:
                click.secho("Veuillez d'abord configurer les groupes avec la commande : 'python cli.py creategroups'", fg="yellow")
                return

            click.echo("Veuillez renseigner les informations suivantes :")
            email = click.prompt("Email")
            if CustomUser.objects.filter(email=email).exists():
                click.secho(f"Un utilisateur avec l'email {email} existe déjà.", fg="red")
                return

            password = click.prompt("Mot de passe",
                                    hide_input=True,
                                    confirmation_prompt="Veuillez répéter le mot de passe pour confirmation")

            employee_number = click.prompt("Numéro d'employé")

            if CustomUser.objects.filter(employee_number=employee_number).exists():
                click.secho(f"Un utilisateur avec le numéro d'employé {employee_number} existe déjà.", fg="red")
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
                        click.secho("Choix invalide. Veuillez sélectionner un numéro valide.", fg="red")
                except ValueError:
                    click.secho("Entrée invalide. Veuillez choisir un département.", fg="red")

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

            click.secho(f"Utilisateur {first_name} {last_name} créé avec succès !", fg="green")

        except Exception as e:
            click.secho(f"Erreur lors de la création de l'utilisateur : {e}", fg="red")


