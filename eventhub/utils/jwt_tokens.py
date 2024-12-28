import json
import requests
import jwt
from datetime import datetime


def save_tokens(access_token, refresh_token):
    tokens = {
        "access": access_token,
        "refresh": refresh_token
    }

    with open (".jwt_tokens", "w") as tokens_file:
        json.dump(tokens, tokens_file)


def get_tokens_from_file():
    try:
        with open(".jwt_tokens", "r") as tokens_file:
            return json.load(tokens_file)
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
    url = "http://127.0.0.1:8000/api/token/refresh/"
    data = {"refresh": refresh_token}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens.get("access")
        new_refresh_token = tokens.get("refresh")

        save_tokens(new_access_token, new_refresh_token)

        print("Le jeton d'accès a été rafraichi !")
        return new_access_token
    else:
        print("Erreur")
        return None

