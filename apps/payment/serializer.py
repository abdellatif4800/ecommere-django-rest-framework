from rest_framework import serializers
from apps.orders.models import OrderList, Order
from .models import Transaction, Init_payment
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
    expiration = serializers.DateTimeField(
        default=timezone.now() + timedelta(hours=1))

    def create(self, validated_data):
        return Init_payment.objects.create(**validated_data)


class TransactionSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    transction_id = serializers.IntegerField()
    paymob_order_id = serializers.IntegerField()

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all())

    success = serializers.BooleanField()

    api_source = serializers.CharField()

    created_at = serializers.DateTimeField()

    amount_cents = serializers.IntegerField()
