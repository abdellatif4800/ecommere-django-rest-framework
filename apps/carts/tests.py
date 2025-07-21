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

from pprint import pprint

from . import models as cart_models
from . import serializer
from apps.products.models import Product
from apps.products.serializer import RetriveProductSerializer


class CartTests(APITestCase):
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
        self.prod_out_of_stock = Product.objects.create(
            name="name",
            descreption="descreption",
            price=5,
            stock=0,
            category="category",
        )

        self.cart_id = res.data["cart"]
        self.access_token = res.data["access"]
        self.cart = get_object_or_404(cart_models.Cart, id=self.cart_id)
        self.cart.cart_total = 20
        # fill cart
        self.item_exist_in_cart = cart_models.CartItem.objects.create(
            product=get_object_or_404(Product, id=1),
            # product=self.prod_out_of_stock,
            quantity=2,
            item_total=10,
            cart=self.cart,
        )

    def test_retrive_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("Retrive_Cart", args=[self.cart_id])
        res = self.client.get(url)
        pprint(dict(res.data))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_add_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse(
            "Add_item_in_cart",
            kwargs={"cart_id": self.cart_id},
        )
        res = self.client.post(url, {"prod_id": 2, "quantity": 2})
        pprint(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_check_out_of_stock(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse(
            "Add_item_in_cart",
            kwargs={"cart_id": self.cart_id},
        )
        res = self.client.post(
            url, {"prod_id": self.prod_out_of_stock.id, "quantity": 2}
        )
        print("Response: ", res.data)
        print("Product: ", RetriveProductSerializer(self.prod_out_of_stock).data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_if_item_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse(
            "Add_item_in_cart",
            kwargs={"cart_id": self.cart_id},
        )
        res = self.client.post(url, {"prod_id": 1, "quantity": 2})
        print("response: ", res.data)
        print(
            "target product: ",
            RetriveProductSerializer(get_object_or_404(Product, id=1)).data,
        )
        print(
            "self.item_exist_in_cart: ",
            serializer.ItemSerializer(self.item_exist_in_cart).data,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse(
            "Change_quantity",
            kwargs={"item_id": 1},
        )
        res = self.client.put(url, {"quantity": 8})
        print("response: ", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse(
            "Delete_item",
            kwargs={"item_id": 1},
        )
        res = self.client.delete(url)
        print(self.cart.cart_total)
        print("response: ", res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
