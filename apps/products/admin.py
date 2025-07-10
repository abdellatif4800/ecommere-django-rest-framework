from django.contrib import admin
from . import models as my_models

# from unfold.admin import ModelAdmin
# from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from django.contrib.postgres.fields import ArrayField
from django.db import models


@admin.register(my_models.Product)
class ProductsAdminSite(admin.ModelAdmin):
    list_display = [
        "name",
        "descreption",
        "price",
        "stock",
        "category",
        "created_at",
        "updated_at",
    ]


@admin.register(my_models.Image)
class ProductsImages(admin.ModelAdmin):
    # readonly_fields = ["product"]
    list_display = ["name", "photo", "product"]
    list_filter = ["product"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["product"]
        return []


# compressed_fields = True
# formfield_overrides = {
#     models.TextField: {
#         "widget": WysiwygWidget,
#     },
#     ArrayField: {
#         "widget": ArrayWidget,
#     },
# }
