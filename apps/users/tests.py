from rest_framework.test import (
    APIClient,
    RequestsClient,
    APIRequestFactory,
    APITestCase,
)
from rest_framework import status

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from pprint import pprint


class UsersTests(APITestCase):
    # def setUp(self):
    # self.new_user = User.objects.create_user(
    #     # username="user101", email="user101@abc.com", password="pass", is_staff=False
    # )

    def signup(self):
        url = reverse("signup")
        data = {"username": "user101", "email": "user101@abc.com", "password": "pass"}
        res = self.client.post(url, data)
        pprint(dict(res.data))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def signin(self):
        # User.objects.create_user(
        #     username="user101", password="pass", email="user101@abc.com"
        # )
        url = reverse("signin")
        data = {
            "username": "user101",
            # "email": "user101@abc.com",
            "password": "pass",
        }
        res = self.client.post(url, data)
        pprint(dict(res.data))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_signup_signin(self):
        print("-------signup -----------")
        self.signup()
        print("------------------")

        print("-------signin-----------")
        self.signin()
        print("------------------")
