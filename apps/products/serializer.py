from .models import Product
from rest_framework import serializers
from django.utils import timezone


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    name = serializers.CharField()
    descreption = serializers.CharField()
    price = serializers.IntegerField()
    stock = serializers.IntegerField()
    category = serializers.CharField()
    image = serializers.URLField(default="")
    created_at = serializers.DateTimeField(default=timezone.now)
    updated_at = serializers.DateTimeField(default=None)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if "name" in validated_data:
            instance.name = validated_data["name"]

        if "descreption" in validated_data:
            instance.descreption = validated_data["descreption"]

        if "price" in validated_data:
            instance.price = validated_data["price"]

        if "stock" in validated_data:
            instance.stock = validated_data["stock"]
        instance.updated_at = timezone.now()
        instance.save()
        return instance
