from rest_framework import serializers
from apps.orders.models import Order
from .models import Transaction, Stripe_checkout, Init_payment
from django.utils import timezone
from datetime import timedelta


class Init_paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Init_payment
        fields = "__all__"

    api_source = serializers.ChoiceField(
        choices=Init_payment.API_SOURCES,
        default=Init_payment.IFRAME,
    )

    payment_link_id = serializers.CharField()

    checkout_link = serializers.CharField()

    amount_cents = serializers.IntegerField()

    created_at = serializers.DateTimeField(default=timezone.now())
    expiration = serializers.DateTimeField(default=timezone.now() + timedelta(hours=1))

    def create(self, validated_data):
        return Init_payment.objects.create(**validated_data)


class Transaction_serialiazer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class Stripe_checkout_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stripe_checkout
        fields = "__all__"

    def create(self, validated_data):
        return Stripe_checkout.objects.create(**validated_data)
