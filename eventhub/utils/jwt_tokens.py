import json
import click
import requests
import jwt
import datetime
from eventhub.models import CustomUser
from decouple import config


SECRET_KEY = config('TOKEN_SECRET_KEY')

TOKENS_FILE = "jwt_tokens.json"

def save_tokens(access_token, refresh_token):
    tokens = {
        "access": access_token,
        "refresh": refresh_token
    }

    with open (TOKENS_FILE, "w") as file:
        json.dump(tokens, file)

def generate_jwt(email, password):

    if not email or not password:
        raise ValueError("Email ou mot de passe manquant.")

    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    refresh_payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token

def get_tokens_from_file():
    try:
        with open(TOKENS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def is_token_expired(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        exp = decoded_token["exp"]
        return datetime.utcfromtimestamp(exp) < datetime.utcnow()
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True


def refresh_access_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")

        user = CustomUser.objects.get(email=email)

        new_access_token, new_refresh_token = generate_jwt(user.email, "dummy_password")

        save_tokens(new_access_token, new_refresh_token)

        click.secho("Le jeton d'accès a été rafraîchi !", fg="green")
        return new_access_token

    except jwt.ExpiredSignatureError:
        click.secho("Le jeton de rafraichissement a expiré. Veuillez vous reconnecter.", fg="red")
        return None

    except jwt.InvalidTokenError:
        click.secho("Le jeton de rafraichissement est invalide. Veuillez vous reconnecter.", fg="red")
        return None

    except CustomUser.DoesNotExist:
        click.secho("L'utilisateur associé au jeton de rafraichissement n'existe pas. Veuillez vous reconnecter.", fg="red")
        return None


def authenticate_user():
    tokens = get_tokens_from_file()

    if not tokens:
        click.secho("Aucun jetons trouvés. Veuillez vous connecter.", fg="red")
        return None

    access_token = tokens.get("access")
    refresh_token = tokens.get("refresh")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")

        user = CustomUser.objects.get(email=email)
        return user

    except jwt.ExpiredSignatureError:
        if refresh_access_token(refresh_token):
            return authenticate_user()
        else:
            click.secho("Le jeton a expiré et n'a pas pu être rafraîchi. Veuillez vous reconnecter.", fg="red")
            return None

    except jwt.InvalidTokenError:
        click.secho("Le jeton est invalide. Veuillez vous reconnecter.", fg="red")
        return None

    except CustomUser.DoesNotExist:
        click.secho("L'utilisateur associé au token n'existe pas. Veuillez vous reconnecter.", fg="red")
        return None


