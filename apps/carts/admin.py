from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin


@admin.register(models.Cart)
class CustomAdminClass(ModelAdmin):
    pass
