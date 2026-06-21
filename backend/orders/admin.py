from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["line_total"]


class StatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ["status", "note", "changed_by", "created_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "payment_method", "total", "created_at"]
    list_filter = ["status", "payment_method", "delivery_type"]
    search_fields = ["order_number", "user__mobile", "user__name"]
    readonly_fields = ["order_number", "subtotal", "total"]
    inlines = [OrderItemInline, StatusHistoryInline]
