from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    item_total = models.IntegerField(default=0)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    cart_total = models.IntegerField(default=0)

    updated_at = models.DateTimeField(null=True)
