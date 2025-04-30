from django.db import models
from django.conf import settings


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    # Optional: link lists to a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='shopping_lists', null=True, blank=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class SavedItem(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    query = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} – ${self.price:.2f}"
