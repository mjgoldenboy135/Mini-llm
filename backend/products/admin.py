from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "category", "price", "stock", "prescription_required", "is_active"]
    list_filter = ["prescription_required", "is_active", "category"]
    search_fields = ["name", "sku", "barcode", "generic_name"]
    list_editable = ["price", "stock", "is_active"]
