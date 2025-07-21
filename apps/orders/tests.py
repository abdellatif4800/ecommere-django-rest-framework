from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.test import (
    APIClient,
    RequestsClient,
    APIRequestFactory,
    APITestCase,
)

from apps.carts import models as cart_models
from . import serializer
from apps.products.models import Product
from apps.products.serializer import RetriveProductSerializer


class OrderTests(APITestCase):
    def setUp(self):
        url = reverse("signup")

        data = {"username": "user101", "email": "user101@abc.com", "password": "pass"}

        res = self.client.post(url, data)

        for _ in range(1, 5):
            Product.objects.create(
                name="name",
                descreption="descreption",
                price=5,
                stock=10,
                category="category",
            )
        self.cart_id = res.data["cart"]
        self.access_token = res.data["access"]
        self.cart = get_object_or_404(cart_models.Cart, id=self.cart_id)

    def test_create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        url = reverse("new-order", args=[self.cart_id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
