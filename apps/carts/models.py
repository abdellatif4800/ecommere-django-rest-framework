from django.db import models
from django.contrib.auth.models import User
from apps.products import models as prod_models


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cart_total = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)


class CartItem(prod_models.BaseItem):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items", null=True
    )
