from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from . import models as my_models

from rest_framework import status
from requests.auth import HTTPBasicAuth
from rest_framework.test import (
    APIClient,
    RequestsClient,
    APIRequestFactory,
    APITestCase,
)

from base64 import b64encode
import json
import os


class ProdTests(APITestCase):
    def setUp(self):
        json_path = os.path.join(os.path.dirname(__file__), "prods.json")
        with open(json_path, "r") as file:
            data = json.load(file)
            for p in data:
                self.prod = my_models.Product.objects.create(
                    name=p["name"],
                    descreption=p["descreption"],
                    price=p["price"],
                    stock=p["stock"],
                    category=p["category"],
                )
                print(f"--{self.prod.id}---", "\n", self.prod, "\n", "-----")
        self.admin_user = User.objects.create_user(
            username="admin", password="pass", is_staff=True
        )

        # self.client.force_authenticate(user=self.admin_user)

        credentials = b64encode(b"admin:pass").decode("utf-8")
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

    def test_create(self):
        res = self.client.post(
            "/product/createProduct/",
            {
                "name": "Smartphone",
                "descreption": "High-end smartphone with 128GB storage",
                "price": 999,
                "stock": 50,
                "category": "Electronics",
            },
            # format="json",
        )
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Smartphone")

    # -----------------------------

    def test_modify(self):
        url = reverse("Update-Product", args=[self.prod.id])
        res = self.client.patch(url, {"stock": 5})
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # -----------------------------

    def test_delete(self):
        url = reverse("Delete-Product", args=[self.prod.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # -----------------------------
    def test_prod_by_id(self):
        # id = os.getenv("prod_id")

        url = reverse("product-by-id", kwargs={"prod_id": 1})
        res = self.client.get(url)
        print(res.data)
        # res = self.client.get(f"/product/productByID/{self.prod.id}/")
        # print(res)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # -----------------------------
    def test_prods_by_catgrories(self):
        url = reverse("by-categories", kwargs={"category": "Smartphone"})
        res = self.client.get(url)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
