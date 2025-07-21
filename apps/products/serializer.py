from .models import Product, Image
from rest_framework import serializers
from django.utils import timezone


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

    def create(self, validate_data):
        image = Image.objects.create(**validate_data)

        return image

    def update(self, instance, validated_data):
        if "name" in validated_data:
            instance.name = validated_data["name"]

        if "photo" in validated_data:
            instance.photo = validated_data["photo"]

        instance.save()
        return instance


class CreateModifyProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        images = self.context.get("request").FILES
        for image in images:
            Image.objects.create(product=product, photo=images.get(image), name=image)

        return product

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


class RetriveProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
