from django.contrib import admin
from . import models as my_models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from django.contrib.postgres.fields import ArrayField
from django.db import models


@admin.register(my_models.Product)
class CustomAdminClass(ModelAdmin):
    compressed_fields = True
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        },
    }
