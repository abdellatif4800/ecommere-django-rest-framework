from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from apps.products import models as prod_models


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    order_total = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    shipping_address = models.TextField(null=False)
    order_notes = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if self.pk and Order.objects.filter(pk=self.pk).exists():
            # Only update when it's not creation
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    #  ------------------------------------
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    # *********************
    ORDER_STATUS = {
        PENDING: "pending",
        PROCESSING: "processing",
        SHIPPED: "shipped",
        DELIVERED: "delivered",
    }
    shipping_status = models.CharField(
        choices=ORDER_STATUS,
        default=PENDING,
    )

    #  ------------------------------------
    CASH_ON_DELIVERY = "cash on delivery"
    BY_CARD = "by card"

    # *********************
    PAYMENT_METHOD = {CASH_ON_DELIVERY: "cash on delivery", BY_CARD: "by card"}
    payment_method = models.CharField(choices=PAYMENT_METHOD, default=CASH_ON_DELIVERY)


class OrderItem(prod_models.BaseItem):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        null=True,
        blank=True,
    )
