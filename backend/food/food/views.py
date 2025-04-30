# hello

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
from django.shortcuts import render
# from django.http import JsonResponse
import requests

# from .utils import get_kroger_access_token
from .forms import KrogerFoodView
from .forms import filter_items_with_pandas
from .utils import fetch_kroger_products

from .models import SavedItem, ShoppingList
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


@csrf_exempt
def save_list(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    data = json.loads(request.body)
    name = data.get('name', '').strip()
    items = data.get('items', [])

    # 1) Create the ShoppingList (only name goes here)
    sl = ShoppingList.objects.create(name=name)

    # 2) Loop over items and create SavedItem for each
    total = 0
    for it in items:
        SavedItem.objects.create(
            shopping_list=sl,      # ForeignKey to the list
            query=it['name'],      # your field for item name
            price=it['price']      # your FloatField
        )
        total += it['price']

    # 3) Return the saved list back to the frontend
    return JsonResponse({
        'id':    sl.id,
        'name':  sl.name,
        'total': total,
        'items': [
            {'name': si.query, 'price': float(si.price)}
            for si in sl.items.all()
        ]
    })


def get_saved_lists(request):
    lists = []
    for sl in ShoppingList.objects.all().order_by('-created_at'):
        # Build a Python list of dicts using the SavedItem.query field
        items = [
            {'name': si.query, 'price': float(si.price)}
            for si in sl.items.all()
        ]
        total = sum(si['price'] for si in items)
        lists.append({
            'id': sl.id,
            'name': sl.name,
            'total': total,
            'items': items
        })
    return JsonResponse(lists, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_list(request, list_id):
    try:
        sl = ShoppingList.objects.get(pk=list_id)
        sl.delete()  # cascades to SavedItem via on_delete=models.CASCADE
        return JsonResponse({'success': True})
    except ShoppingList.DoesNotExist:
        return JsonResponse({'error': 'List not found'}, status=404)
