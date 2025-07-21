from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Cart, CartItem
from apps.products.models import Product
from apps.carts import models
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    cart_items = ItemSerializer(many=True, read_only=True)
    cart_total = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(default=None)

    def update(self, instance, validated_data):
        if "cart_total" in validated_data:
            instance.cart_total = validated_data["cart_total"]

        if "items" in validated_data:
            instance.items = validated_data["items"]

        instance.updated_at = timezone.now()
        instance.save()
        return instance
