from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
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
    verbose_name = "cart_items"
    related_name = "cart_items"
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
    model = models.CartItem
    extra = 0


@admin.register(models.Cart)
class CustomAdminClass(ModelAdmin):
    list_display = ["id", "user", "cart_total", "updated_at"]
    inlines = [ItemsTabularInline]
    list_sections = [
        ItemsTableSection,
    ]
