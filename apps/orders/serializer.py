from .models import OrderList, Order
from apps.carts.models import Item
from apps.products.models import Product
from apps.users.models import User
from rest_framework import serializers
from django.utils import timezone


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    orders = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), many=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    items = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), many=True)
    order_tota = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(default=None)
    updated_at = serializers.DateTimeField(default=None)
    shipping_address = serializers.CharField()
    order_notes = serializers.CharField()
    shipping_status = serializers.ChoiceField(
        choices=Order.ORDER_STATUS, default=Order.PENDING
    )
    payment_method = serializers.ChoiceField(
        choices=Order.PAYMENT_METHOD, default=Order.CASH_ON_DELIVERY
    )

    # def create(self, validated_data):
    #     return Cart.objects.create(**validated_data)
    #
    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        instance.save()
        return instance
