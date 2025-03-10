# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_staff",
        "is_superuser",
        "avatar",
    )
    list_filter = [
        "organisms",
    ]


admin.site.register(User, UserAdmin)
