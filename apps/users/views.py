from django.shortcuts import render
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.orders.models import OrderList
from apps.orders.serializer import OrderListSerializer
from apps.carts.models import Cart
from apps.carts.serializer import CartSerializer
from . import serializer


class UserRegiester(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
        )

        cart = Cart.objects.create(user=user)
        order = OrderList.objects.create(user=user)
        return Response(
            {
                "user": serializer.UserSerializer(user).data,
                "cart": CartSerializer(cart).data,
                "order": OrderListSerializer(order).data,
            }
        )


class Signin(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )
        if not user.is_active:
            raise AuthenticationFailed("Invalid credentials")
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                # "user": serializer.UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
