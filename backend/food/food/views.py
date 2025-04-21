# hello

from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.shortcuts import render
# from django.http import JsonResponse
import requests

# from .utils import get_kroger_access_token
from .forms import KrogerFoodView
from .forms import filter_items_with_pandas
from .utils import fetch_kroger_products

from .models import SavedItem
from django.views.decorators.csrf import csrf_exempt


import pandas as pd
import os


def home_page(request):
    return render(request, "home.html")


def search_items(request):
    # Ensure we're getting the parameters from the GET request
    query = request.GET.get("query", "")
    budget = request.GET.get("budget", None)

    print("Received query:", query)
    print("Received budget:", budget)

    items = fetch_kroger_products(query)
    # print(f"Total Kroger items returned: {len(items)}")

    # filtered = filter_items_with_pandas(items, budget=budget, keyword=query)

    # Transform the items to match frontend expectations
    # Directly use the already formatted data
    # items = fetch_kroger_products(query)

    return JsonResponse({
        "items": items,
        "query": query,
        "budget": budget
    })


@csrf_exempt
# Function for adding from Database
def add_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        price = data.get("price")

        item = SavedItem.objects.create(query=query, price=price)
        return JsonResponse({"message": "Item added", "item": {"id": item.id, "query": item.query, "price": item.price}})


def get_items(request):
    items = SavedItem.objects.all().order_by("-added_at")
    data = [{"id": item.id, "query": item.query, "price": item.price}
            for item in items]
    return JsonResponse({"items": data})

# Function for deleting from Database


@csrf_exempt
def delete_item(request, item_id):
    if request.method == "DELETE":
        try:
            item = SavedItem.objects.get(id=item_id)
            item.delete()
            return JsonResponse({"message": "Item deleted"})
        except SavedItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
