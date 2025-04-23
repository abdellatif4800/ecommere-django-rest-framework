from django.shortcuts import render
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from pprint import pprint
import bcrypt
from .helper import generate_token


class UserRegiester(APIView):
    # with APIView
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
