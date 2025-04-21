from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class SavedItem(models.Model):
    Listname = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} - ${self.price}"
