from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

# from apps.orders.models import OrderList
# from apps.orders.serializer import OrderListSerializer
from apps.carts.models import Cart
from apps.carts.serializer import CartSerializer
from . import serializer


class UserRegiester(APIView):
    def post(self, request):
        try:
            user = User.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                password=request.data["password"],
            )

            cart = Cart.objects.create(user=user)
            if user is None:
                raise AuthenticationFailed("Invalid credentials")

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_409_CONFLICT)


class Signin(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )
        if user is None:
            raise AuthenticationFailed("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        cart = get_object_or_404(Cart, user=user.id)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "cart_id": cart.id,
                },
            }
        )
