from django.shortcuts import render
from .serializer import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from pprint import pprint
from rest_framework.generics import ListAPIView, RetrieveAPIView


class Product_management(APIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, prod_id):
        prod = Product.objects.get(id=prod_id)
        serializer = ProductSerializer(prod, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, prod_id):
        prod = Product.objects.get(id=prod_id)
        prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class Product_retrive(APIView):
#     def get(self, request, prod_id):
#         prod = Product.objects.get(id=prod_id)
#         print("asd")
#
#         serializer = ProductSerializer(prod)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def get(self, request):
#         prod = Product.objects.all()
#         serializer = ProductSerializer(prod, many=True)
#         return Response(serializer.data)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
