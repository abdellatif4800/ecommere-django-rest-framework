from django.db import models
from django.utils import timezone


class Init_payment(models.Model):
    QUICKLINK = "quick_link"
    INVOICE = "invoice"
    IFRAME = "iframe"

    # *********************
    API_SOURCES = {QUICKLINK: "quick_link", INVOICE: "invoice", IFRAME: "iframe"}

    api_source = models.CharField(
        choices=API_SOURCES,
        default=IFRAME,
    )
    paymob_order_id = models.IntegerField(null=True, blank=True)
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, null=True, unique=True
    )

    status = models.CharField(default="UNPAID")
    payment_link_id = models.TextField()
    checkout_link = models.TextField()

    amount_cents = models.IntegerField()

    created_at = models.DateTimeField()
    expiration = models.DateTimeField()


class Stripe_checkout(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, null=False)

    payment_link = models.URLField(max_length=1000, null=False)
    success_url = models.URLField(
        max_length=1000, null=False, default="http://example.com/success"
    )

    amount = models.IntegerField(null=False)

    stripe_checkout_id = models.CharField(null=False)

    has_paid = models.BooleanField(null=False)

    created_at = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField(null=False)


class Transaction(models.Model):
    provider = models.CharField(null=False, default="stripe")

    transction_id = models.IntegerField(null=False)

    success = models.BooleanField(null=False)

    amount = models.IntegerField(null=False)

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, null=False)

    created_at = models.DateTimeField(default=timezone.now)
