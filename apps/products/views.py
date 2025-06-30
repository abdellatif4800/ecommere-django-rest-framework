from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import CreateModifyProductSerializer, RetriveProductSerializer
from .models import Image, Product
from .images_handler import saveImages

from pprint import pprint




class Create_product(CreateAPIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAdminUser, IsAuthenticated]

    serializer_class = CreateModifyProductSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CreateModifyProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            if request.FILES:
                saveImages(request.FILES, serializer.data["id"])

            
            return Response(
                {
                    "data": serializer.data,
                 
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Update_product(UpdateAPIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CreateModifyProductSerializer
    parser_classes = [FormParser]

    def put(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs["prod_id"])
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CreateModifyProductSerializer(
            product, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Delete_product(DestroyAPIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = RetriveProductSerializer

    def delete(self, request, prod_id):
        try:
            product = Product.objects.get(id=prod_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesListView(ListAPIView):
    serializer_class = RetriveProductSerializer

    def get_queryset(self):
        category = self.kwargs["category"]
        return Product.objects.filter(category=category)

    def list(self, request, *args, **kwargs):
        prods_list = cache.get_or_set(
            f"categories:{kwargs['category']}",
            lambda: RetriveProductSerializer(self.get_queryset(), many=True).data,
            timeout=60 * 5,
        )

        return Response(prods_list)


class Product_by_id(RetrieveAPIView):
    serializer_class = RetriveProductSerializer

    def get(self, request, prod_id):
        try:
            target_prod = cache.get_or_set(
                f"product:{prod_id}",
                lambda: RetriveProductSerializer(Product.objects.get(id=prod_id)).data,
                timeout=60 * 5,
            )
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(target_prod, status=status.HTTP_200_OK)
