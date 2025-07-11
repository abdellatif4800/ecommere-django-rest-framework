from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from . import models as my_models

from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.sections import TableSection, TemplateSection
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from unfold.decorators import action
from unfold.components import BaseComponent, register_component

from django.utils.html import format_html


class ImagesTableSection(TableSection):
    verbose_name = "images"
    related_name = "images"
    fields = ["name", "photo_url"]

    def images_field(self, instance):
        return instance.pk


class ImagesTabularInline(TabularInline):
    model = my_models.Image
    extra = 0


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
