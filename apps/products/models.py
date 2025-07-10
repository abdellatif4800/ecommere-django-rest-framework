from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField()
    descreption = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True)


class Image(models.Model):
    name = models.CharField(max_length=255, default="Main Image")
    photo = models.ImageField(upload_to="products/")
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
