from apps.carts.serializer import CartSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order_Item, OrderList, Order
from apps.carts.models import Cart
from .serializer import OrderListSerializer, OrderSerializer
from django.utils import timezone


class OrderList_view(APIView):
    def get(self, request):
        user_id = int(request.query_params.get("user_id"))
        target_orderList = OrderList.objects.get(user=user_id)
        target_cart = Cart.objects.get(user=user_id)
        return Response(
            {
                "orderList": OrderListSerializer(target_orderList).data,
            }
        )


class Order_view(APIView):
    def post(self, request):
        user_id = int(request.query_params.get("user_id"))
        target_orderList = OrderList.objects.get(user=user_id)
        target_cart = Cart.objects.get(user=user_id)

        payment_method = request.data['payment_method']

        if len(target_cart.items.all()) != 0:
            new_order = Order.objects.create(
                order_total=target_cart.cart_total,
                created_at=timezone.now(),
            )

            for item in target_cart.items.all():
                new_order_item = Order_Item.objects.create(
                    product=item.product, quantity=item.quantity, item_total=item.item_total
                )
                new_order.items.add(new_order_item)

            new_order.payment_method = payment_method
            if payment_method == "cash on delivery":
                new_order.shipping_status = "processing"
                new_order.save()
            elif payment_method == "by card":
                new_order.shipping_status = "pending"
                new_order.save()

            target_orderList.orders.add(new_order)

            for item in target_cart.items.all():
                target_cart.items.remove(item)
                item.delete()
                target_cart.cart_total = 0
            target_cart.save()
            return Response(
                {
                    "orderList": OrderListSerializer(target_orderList).data,
                    "cart": CartSerializer(target_cart).data,
                }
            )
        if len(target_cart.items.all()) == 0:

            return Response(
                {
                    "msg": "Cart is empty"

                }
            )
