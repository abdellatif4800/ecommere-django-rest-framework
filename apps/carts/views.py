from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)


from apps.products.models import Product
from apps.products.serializer import RetriveProductSerializer
from .serializer import CartSerializer, ItemSerializer
from .models import Cart, CartItem

from pprint import pprint


class Retrive_Cart(RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    # lookup_field = "id"

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        target_cart = cache.get_or_set(
            f"carts:{id}",
            lambda: CartSerializer(Cart.objects.get(id=id)).data,
            timeout=60 * 5,
        )
        return Response(target_cart, status=status.HTTP_200_OK)


class Add_item_in_cart(CreateAPIView):
    serializer_class = ItemSerializer
    queryset = CartItem.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs["cart_id"])
        product = get_object_or_404(Product, id=request.data["prod_id"])
        # --------------------------
        for prod in CartSerializer(cart).data["cart_items"]:
            if product.id == prod["product"]:
                return Response(
                    "product exist in cart", status=status.HTTP_400_BAD_REQUEST
                )
        if product.stock == 0:
            return Response("product out of stock", status=status.HTTP_400_BAD_REQUEST)
        # --------------------------

        data = {
            "cart": cart.id,
            "product": product.id,
            "quantity": int(request.data["quantity"]),
            "item_total": int(request.data["quantity"]) * int(product.price),
        }

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            product.stock -= int(request.data["quantity"])
            cart.cart_total += data["item_total"]
            serializer.save()
            cart.save()
            product.save()

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "cart": CartSerializer(cart).data,
                # "prod": RetriveProductSerializer(product).data,
            },
            status=status.HTTP_201_CREATED,
        )


class Change_quantity(UpdateAPIView):
    serializer_class = ItemSerializer
    queryset = CartItem.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        item = get_object_or_404(CartItem, id=kwargs["item_id"])
        product = item.product
        cart = item.cart
        quantity = int(request.data["quantity"])

        if product.stock == 0 or product.stock < 0:
            return Response(
                "quantity not acceptable", status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock:
            return Response(
                "quantity greater than product stock",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if item.quantity == quantity:
            return Response("no changes")

        if quantity < item.quantity:
            diff = item.quantity - quantity
            product.stock += diff
            cart.cart_total -= diff * product.price
        elif quantity > item.quantity:
            diff = quantity - item.quantity
            product.stock -= diff
            cart.cart_total += diff * product.price

        item.item_total = quantity * product.price
        item.quantity = quantity

        item.save()
        product.save()
        cart.save()

        return Response(
            {
                "item": ItemSerializer(item).data,
                "prod": RetriveProductSerializer(product).data,
            },
            status=status.HTTP_200_OK,
        )


class Delete_item(DestroyAPIView):
    serializer_class = ItemSerializer
    queryset = CartItem.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        item = get_object_or_404(CartItem, id=kwargs["item_id"])
        cart = item.cart
        product = item.product

        for prod in CartSerializer(cart).data["cart_items"]:
            if product.id == prod["product"]:
                product.stock += item.quantity
                cart.cart_total -= item.item_total
                # print(product.stock)
                item.delete()
                cart.save()
                product.save()

                return Response({"cart": CartSerializer(cart).data}, status.HTTP_200_OK)
