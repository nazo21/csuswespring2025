# utils.py

import requests
from requests.auth import HTTPBasicAuth


def get_kroger_access_token(client_id, client_secret):
    url = "https://api-ce.kroger.com/v1/connect/oauth2/token"
    # access_token = get_kroger_access_token(client_id, secret_kroger_key)
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

# kroger_api.py or utils.py


def get_location_id_by_zip(*zip_code):
    access_token = get_kroger_access_token(client_id, secret_kroger_key)

    url = "https://api-ce.kroger.com/v1/locations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    params = {
        "filter.zipCode.near": zip_code,
        "filter.limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to get location ID: {response.status_code}")
        return None

    locations = response.json().get("data", [])
    if not locations:
        print("No location found near this ZIP.")
        return None

    return locations[0]["locationId"]


# Valid 8-character store ID (e.g., Midtown Cleveland Kroger) ): # Valid 8-character store ID (e.g., Midtown Cleveland Kroger)):
def fetch_kroger_products(query):
    access_token = get_kroger_access_token(client_id, secret_kroger_key)

    url = "https://api-ce.kroger.com/v1/products"

    location_id = get_location_id_by_zip("45459", "43215", "92507")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    params = {
        "filter.term": query,
        "filter.limit": 50,
        "filter.locationId": location_id  # Use this if you want prices specific to a store
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch from Kroger: {response.status_code}")
        return []

    products = response.json().get("data", [])
    formatted_items = []

    for product in products:
        name = product.get("description", "No name")
        price = None

        try:
            item = product["items"][0]
            price_info = item.get("price", {})
            price = price_info.get("promo") or price_info.get("regular")
        except (IndexError, KeyError, TypeError):
            price = None

        if price is None:
            # Debugging line to see missing prices
            print(f"Price not found for product: {name}")

        if price:
            formatted_items.append({
                "name": name,
                "price": round(float(price), 2)
            })

    return formatted_items
