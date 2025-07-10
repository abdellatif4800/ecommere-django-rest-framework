from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

# from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
# from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class StaffAdmin(BaseUserAdmin, admin.ModelAdmin):
    def get_list_display(self, request):
        exclude_fields = ["password"]
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in exclude_fields
        ]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, admin.ModelAdmin):
    pass
