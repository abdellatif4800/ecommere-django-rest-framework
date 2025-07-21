from .models import Order, OrderItem
from apps.products.models import Product

from rest_framework import serializers
from rest_framework import status

from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        # read_only_fields = ["shipping_status"]

    order_items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")

        if validated_data["payment_method"] == "by card":
            validated_data["shipping_status"] = "processing"

        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        instance.save()
        return instance
