from apps.carts.models import Cart
from django.shortcuts import render
from .serializer import UserSerializer, SignInSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from pprint import pprint
import bcrypt
from .helper import generate_token
from apps.orders.models import OrderList
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
sudo apt update
sudo apt install build-essential

class UserRegiester(APIView):
    @swagger_auto_schema(operation_description="User Register",  request_body=UserSerializer, responses={200: UserSerializer(many=True)})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Cart.objects.create(user=user)
            OrderList.objects.create(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)


class Signin(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data["email"]).first()
        serializer = UserSerializer(user)
        # ----------- verify password ---------------
        db_password = serializer.data["password"].encode("utf-8")
        user_password = request.data["password"].encode("utf-8")

        check_pass = bcrypt.checkpw(user_password, db_password)
        # -------------------------------------------
        if check_pass:
            print(user.first_name)
            return Response(
                {
                    "token": generate_token(
                        {
                            "id": serializer.data["id"],
                            "username": user.username,
                            "email": serializer.data["email"],
                        }
                    )
                }
            )
        else:
            return Response("pass not vaild")


# user = User.objects.create_user(
    # username="name103", password="pass123")
    # username="admin101", password="pass123", is_superuser=True, is_staff=True)

# user.save()
# u = User.objects.get(username="name103")
# u = authenticate(username="name103", password="pass123")
# token = Token.objects.create(user=u)
print("************************")
# print(u)
# print(token.key)
print("************************")
