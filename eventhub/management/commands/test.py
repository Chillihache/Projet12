from django.core.management.base import BaseCommand
from eventhub.utils.api_requests import make_authenticated_request


class Command(BaseCommand):
    help = "Test d'une requête authentifée"

    def handle(self, *args, **kwargs):
        url = 'http://127.0.0.1:8000/api/test/'
        response = make_authenticated_request(url)

        if response and response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(f"Réponse : {response.json()}"))
        elif response:
            self.stdout.write(self.style.ERROR(f"Erreur : {response.status_code}"))
        else:
            self.stdout.write(self.style.ERROR("Échec de la requête."))