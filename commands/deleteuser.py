import click
from eventhub.utils.jwt_tokens import authenticate_user
from eventhub.models import CustomUser


@click.command()
@click.argument("email")
def deleteuser(email):
    user = authenticate_user()

    if user:
        if not user.is_superuser and not user.has_perm('eventhub.delete_customuser'):
            click.echo("Vous n'avez pas la permission de supprimer un utilisateur")
            return

        user_to_delete = CustomUser.objects.filter(email=email).first()

        if not user_to_delete:
            click.echo("Cet email ne correspond a aucun utilisateur")
            return

        if not click.confirm(f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user_to_delete.first_name} {user_to_delete.last_name} ?"):
            click.echo("Suppression annulée.")
            return

        user_to_delete.delete()

        click.echo("L'utilisateur a été supprimé !")