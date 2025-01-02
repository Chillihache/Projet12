import requests
from eventhub.utils.jwt_tokens import get_tokens_from_file, is_token_expired, refresh_access_token


def make_authenticated_request(url, method="GET", data=None):
    tokens = get_tokens_from_file()

    if tokens:
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        if is_token_expired(access_token):
            print("Le jeton d'accès a expiré. Rafraichissement en cours...")
            access_token = refresh_access_token(refresh_token)

            if not access_token:
                print("Veuillez vous reconnecter")
                return None

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = getattr(requests, method.lower())(url, headers=headers, data=data)

        return response

    else:
        print("Pas de jeton trouvé, Veuillez vous connecter")
        return None
