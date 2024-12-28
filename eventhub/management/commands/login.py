import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from eventhub.utils.jwt_tokens import save_tokens


class Command(BaseCommand):
    help = "Authentifie un utilisateur et génère un jeton JWT"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Adresse email")
        parser.add_argument("password", type=str, help="Mot de passe")


    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        password = kwargs["password"]

        response = requests.post(
            'http://127.0.0.1:8000/api/token/',
            data={'email': email, 'password': password}
        )

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')

            save_tokens(access_token, refresh_token)
            self.stdout.write(self.style.SUCCESS('Connexion réussie !'))
        else:
            self.stdout.write(self.style.ERROR('Connextion échouée.'))