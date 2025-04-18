# hello
import requests
from django.http import JsonResponse
from .utils import get_kroger_access_token
import os
client_id = 'nazeerahmad-243261243034247534474c336551586966456b514e4b694b774e494f2e684e65387571744149726d5576744773567a74486b6e434b314b3371466b4b8212988171852896486'

secret_kroger_key = 'aocx6Pr1qFFN6ZxBe-QfOGBnmeQVClClGHaW89A1'

token = get_kroger_access_token(client_id, secret_kroger_key)


def KrogerFoodView(request):
    try:
        # Get your access token
        access_token = get_kroger_access_token(client_id, secret_kroger_key)
        # Example API call to search for products
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        params = {
            "filter.term": "milk",     # You can change this to anything
            "filter.limit": 5,
            "filter.locationId": "01500835"  # Replace with a real location ID
        }
        response = requests.get(
            "https://api.kroger.com/v1/products", headers=headers, params=params)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Failed to fetch products", "details": response.text}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
