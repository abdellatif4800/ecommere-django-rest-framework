from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField()
    descreption = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.CharField()
    image = models.URLField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)
