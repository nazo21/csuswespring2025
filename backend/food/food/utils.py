# utils.py

import requests
from requests.auth import HTTPBasicAuth


def get_kroger_access_token(client_id, client_secret):
    url = "https://api-ce.kroger.com/v1/connect/oauth2/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }

    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(url, headers=headers, data=data, auth=auth)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(
            f"Failed to get token: {response.status_code}, {response.text}")
