from apps.products.models import Product
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import CartSerializer, ItemSerializer
from rest_framework.decorators import api_view
from .models import Cart, Item
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from apps.products.serializer import ProductSerializer
from rest_framework import status
from django.utils import timezone
from pprint import pprint
from .permissions import CustomerAccessPermission
from django.contrib.auth import authenticate, login


class Cart_view(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        user = authenticate(request, username="asd", password="pass")
        if user is not None:
            print(user)

        user_id = int(request.query_params.get("user_id"))
        target_cart = Cart.objects.get(user=user_id)
        all_items = []
        for item in target_cart.items.all():
            all_items.append(ItemSerializer(item).data)

        return Response(
            {
                "msg": "cart found",
                "cart": CartSerializer(target_cart).data,
                "all items in detail": all_items,
            },
            status=status.HTTP_200_OK,
        )


class Item_view(APIView):
    def post(self, request):
        user_id = int(request.query_params.get("user_id"))
        prod_id = int(request.query_params.get("prod_id"))

        target_product = Product.objects.get(id=prod_id)
        target_cart = Cart.objects.get(user=user_id)
        # --------------------------------
        items_prod_ids = []
        for item in target_cart.items.all():
            items_prod_ids.append(item.product.id)
        # --------------------------------
        if target_product.stock == 0:

            return Response(
                {
                    "msg": f"prod with id {prod_id} is out of stock",
                    "product": ProductSerializer(target_product).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if prod_id in items_prod_ids:
            return Response(
                {
                    "msg": f"prod with id {prod_id} is aleardy in cart",
                    "cart": CartSerializer(target_cart).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if prod_id not in items_prod_ids:
            new_item = Item.objects.create(
                product=target_product,
                quantity=request.data["quantity"],
                item_total=target_product.price * request.data["quantity"],
            )
            target_cart.items.add(new_item)
            target_cart.cart_total += new_item.item_total
            target_cart.updated_at = timezone.now()

            target_cart.save()
            return Response(
                {
                    "cart": CartSerializer(target_cart).data,
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request):
        user_id = int(request.query_params.get("user_id"))
        prod_id = int(request.query_params.get("prod_id"))
        item_id = int(request.query_params.get("item_id"))
        # -------------------------------
        target_product = Product.objects.get(id=prod_id)
        target_cart = Cart.objects.get(user=user_id)
        target_item = Item.objects.get(id=item_id)
        cart_data = CartSerializer(target_cart).data

        # --------------------------------
        items_prod_ids = []
        for item in target_cart.items.all():
            items_prod_ids.append(item.product.id)
        # ----------------------------
        if prod_id in items_prod_ids:
            target_cart.cart_total -= target_item.item_total

            target_cart.items.remove(target_item)
            target_item.delete()
            target_cart.updated_at = timezone.now()

            target_cart.save()

            return Response(
                {
                    "msg": f"prod with id {prod_id} deleted from cart",
                    "cart": CartSerializer(target_cart).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if prod_id not in items_prod_ids:

            return Response(
                {
                    "cart": CartSerializer(target_cart).data,
                },
                status=status.HTTP_200_OK,
            )


@api_view(["PUT"])
def change_quantity(request):
    user_id = int(request.query_params.get("user_id"))
    item_id = int(request.query_params.get("item_id"))
    target_cart = Cart.objects.get(user=user_id)
    target_item = Item.objects.get(id=item_id)
    cart_data = CartSerializer(target_cart).data

    # --------------------------------
    items_prod_ids = []
    for item in target_cart.items.all():
        items_prod_ids.append(item.product.id)
        # ----------------------------
        if request.data["quantity"] == 0 or request.data["quantity"] < 0:
            return Response("quantity value not acceptaple")
        if request.data["quantity"] > target_item.product.stock:
            return Response(
                {
                    "massage": f"product with id {target_item.product.id} have {target_item.product.stock} in the stock"
                }
            )
        target_item.quantity = request.data["quantity"]
        target_item.item_total = request.data["quantity"] * \
            target_item.product.price
        print(target_item.product.stock)
        return Response(ItemSerializer(target_item).data)
