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
from rest_framework.pagination import PageNumberPagination

from .serializer import (
    CreateModifyProductSerializer,
    RetriveProductSerializer,
    ImageSerializer,
)
from .models import Image, Product
from .images_handler import saveImages

from pprint import pprint


class Create_product(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = CreateModifyProductSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Product.objects.all()


class Update_product(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateModifyProductSerializer
    lookup_field = "id"

    parser_classes = [MultiPartParser]

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]


class Delete_product(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = RetriveProductSerializer
    lookup_field = "id"

    parser_classes = [MultiPartParser]

    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [BasicAuthentication]


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


class AddNewImage(CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    parser_classes = [MultiPartParser]

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]


class UpdateNewImage(UpdateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    lookup_field = "id"

    parser_classes = [MultiPartParser]

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
