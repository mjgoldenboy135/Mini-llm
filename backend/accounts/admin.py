from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["mobile", "name", "email", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active"]
    search_fields = ["mobile", "name", "email"]
    ordering = ["-date_joined"]
    fieldsets = (
        (None, {"fields": ("mobile", "password")}),
        ("Personal info", {"fields": ("name", "email", "avatar")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("mobile", "name", "password1", "password2")}),
    )


@admin.register(OTPVerification)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["mobile", "code", "is_used", "created_at"]
