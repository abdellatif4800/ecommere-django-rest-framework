from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


from apps.carts import serializer as carts_serializer
from apps.carts.models import Cart, CartItem
from .models import OrderItem, Order
from .serializer import OrderSerializer, OrderItemSerializer


class Create_order(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs["cart_id"])

        items = CartItem.objects.filter(cart=kwargs["cart_id"])

        if not items.exists():
            return Response("No items", status=status.HTTP_400_BAD_REQUEST)

        order_items_data = []

        for item in items:
            order_items_data.append(
                {
                    "product": item.product.id,
                    "quantity": item.quantity,
                    "item_total": item.item_total,
                }
            )

        data = {
            **request.data,
            "user": request.user.id,
            "order_total": cart.cart_total,
            "order_items": order_items_data,
        }

        if items.exists():
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                order = serializer.save()

                if order is not None:
                    for item in items:
                        item.delete()

                cart.cart_total = 0
                cart.save()

                return Response(
                    {
                        "order": OrderSerializer(order).data,
                    }
                )
            else:
                print(serializer.data)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Retrive_order(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = "id"

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
