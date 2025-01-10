import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import CustomUser


@click.command()
@click.argument("email")
def deleteuser(email):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.delete_customuser'):
            click.secho("Vous n'avez pas la permission de supprimer un utilisateur.", fg="red")
            return

        user_to_delete = CustomUser.objects.filter(email=email).first()

        if not user_to_delete:
            click.secho("Cet email ne correspond a aucun utilisateur.", fg="red")
            return

        if not click.confirm(f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user_to_delete.first_name} {user_to_delete.last_name} ?"):
            click.secho("Suppression annulée.", fg="yellow")
            return

        user_to_delete.delete()

        click.secho("L'utilisateur a été supprimé !", fg="red")