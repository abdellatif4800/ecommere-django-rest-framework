from django.db import models


class Order_Item(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    item_total = models.IntegerField(default=0)


class Order(models.Model):
    items = models.ManyToManyField(Order_Item)
    order_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    shipping_address = models.TextField(null=True)
    order_notes = models.TextField(null=True)
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

    ORDER_STATUS = {
        PENDING: "pending",
        SHIPPED: "shipped",
        DELIVERED: "delivered",
    }
    shipping_status = models.CharField(
        choices=ORDER_STATUS,
        default=PENDING,
    )
    CASH_ON_DELIVERY = "cash on delivery"
    VISA = "visa"

    PAYMENT_METHOD = {CASH_ON_DELIVERY: "cash on delivery", VISA: "visa"}
    payment_method = models.CharField(
        choices=PAYMENT_METHOD, default=CASH_ON_DELIVERY)


class OrderList(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
