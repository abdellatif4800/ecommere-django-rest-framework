from django.contrib import admin
from . import models
from apps.orders import models as order_models

from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    BooleanRadioFilter,
    ChoicesRadioFilter,
    ChoicesCheckboxFilter,
    TextFilter,
    FieldTextFilter,
)
from unfold.admin import StackedInline, TabularInline
from unfold.sections import TableSection
from unfold.contrib.inlines.admin import NonrelatedTabularInline


@admin.register(models.Stripe_checkout)
class Stripe_checkout_admin(ModelAdmin):
    list_display = [
        "id",
        "order",
        "amount",
        "stripe_checkout_id",
        "has_paid",
        "created_at",
        "expiration",
    ]

    list_filter_submit = True
    list_filter = [
        ("has_paid", BooleanRadioFilter),
    ]
