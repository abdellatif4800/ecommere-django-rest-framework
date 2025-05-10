from django.db import models


class Init_payment(models.Model):

    QUICKLINK = "quick_link"
    INVOICE = "invoice"
    IFRAME = "iframe"

    # *********************
    API_SOURCES = {
        QUICKLINK: "quick_link", INVOICE: "invoice", IFRAME: "iframe"

    }

    api_source = models.CharField(
        choices=API_SOURCES,
        default=IFRAME,
    )
    paymob_order_id = models.IntegerField(null=True, blank=True)
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, null=True, unique=True)

    status = models.CharField(default="UNPAID")
    payment_link_id = models.TextField()

    checkout_link = models.TextField()

    amount_cents = models.IntegerField()

    created_at = models.DateTimeField()
    expiration = models.DateTimeField()


class Transaction(models.Model):
    transction_id = models.IntegerField()
    paymob_order_id = models.IntegerField()

    success = models.BooleanField()

    api_source = models.CharField()

    amount_cents = models.IntegerField()

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)

    created_at = models.DateTimeField()
