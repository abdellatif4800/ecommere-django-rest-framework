from django.contrib import admin
from . import models
from apps.payment import models as payment_models

from unfold.admin import TabularInline, ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.sections import TableSection, TemplateSection
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from unfold.decorators import action
from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import (
    BooleanRadioFilter,
    ChoicesRadioFilter,
    ChoicesCheckboxFilter,
    TextFilter,
    FieldTextFilter,
)


class ItemsTableSection(TableSection):
    verbose_name = "order_items"
    related_name = "order_items"
    fields = [
        "id",
        "product",
        "product_price",
        "quantity",
        "item_total",
    ]

    def cart_items_field(self, instance):
        return instance.pk

    def product_price(self, instance):
        return instance.product.price

    product_price.short_description = "Price"


class ItemsTabularInline(TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class CustomOrderClass(ModelAdmin):
    list_display = ["id", "user", "order_total", "created_at", "updated_at"]
    inlines = [
        ItemsTabularInline,
    ]
    list_sections = [
        ItemsTableSection,
    ]
