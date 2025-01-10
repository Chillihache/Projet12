import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import CustomUser


@click.command()
@click.argument("email")
def updateuser(email):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.change_customuser'):
            click.secho("Vous n'avez pas la permission de modifier un utilisateur.", fg="red")
            return

        user_to_update = CustomUser.objects.filter(email=email).first()

        if not user_to_update:
            click.secho("Cet email ne correspond à aucun utilisateur.", fg="red")
            return

        click.echo(f"Modification des informations de l'utilisateur {user_to_update.first_name} {user_to_update.last_name}.\n"
                   "Laissez vides les champs que vous ne souhaitez pas modifier.")

        new_email = click.prompt("Nouvel email", default=user_to_update.email)
        new_first_name = click.prompt("Nouveau prénom", default=user_to_update.first_name)
        new_last_name = click.prompt("Nouveau nom", default=user_to_update.last_name)
        new_password = click.prompt("Nouveau mot de passe (laisser vide pour ne pas changer)", default="", hide_input=True)
        new_employee_number = click.prompt("Nouveau numéro d'employé", default=user_to_update.employee_number)

        try:
            user_to_update.email = new_email
            user_to_update.first_name = new_first_name
            user_to_update.last_name = new_last_name
            user_to_update.employee_number = new_employee_number
            if new_password:
                user_to_update.set_password(new_password)
            user_to_update.save()

            click.secho(f"Les informations de l'utilisateur {user_to_update.first_name} {user_to_update.last_name} ont été mises à jour avec succès.", fg="green")

        except Exception as e:
            click.secho(f"Erreur lors de la mise à jour de l'utilisateur : {e}", fg="red")
