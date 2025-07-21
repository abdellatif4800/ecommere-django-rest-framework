from django.contrib import admin
from django.core.validators import EMPTY_VALUES
from . import models as my_models

from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.sections import TableSection, TemplateSection
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from unfold.decorators import action

# from unfold.components import BaseComponent, register_component
from unfold.contrib.filters.admin import (
    BooleanRadioFilter,
    ChoicesRadioFilter,
    ChoicesCheckboxFilter,
    TextFilter,
    FieldTextFilter,
)


class ImagesTableSection(TableSection):
    verbose_name = "images"
    related_name = "images"
    fields = ["name", "photo_url"]

    def images_field(self, instance):
        return instance.pk


class ImagesTabularInline(TabularInline):
    model = my_models.Image
    extra = 0


class CustomTextFilter(TextFilter):
    title = "Custom filter"
    parameter_name = "query_param_in_uri"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            # Here write custom query
            return queryset.filter(category=self.value())

        return queryset


@admin.register(my_models.Product)
class ProductsAdminSite(ModelAdmin):
    inlines = [ImagesTabularInline]
    list_display = [
        "name",
        "id",
        "descreption",
        "price",
        "stock",
        "category",
        "created_at",
        "updated_at",
    ]

    list_sections = [
        ImagesTableSection,
    ]

    exclude = [
        "created_at",
        "updated_at",
    ]
    list_filter_submit = True
    list_filter = [CustomTextFilter]
