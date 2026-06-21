import uuid
from django.db import models
from django.conf import settings


class SalesSummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(unique=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_items_sold = models.PositiveIntegerField(default=0)
    new_customers = models.PositiveIntegerField(default=0)
    prescription_orders = models.PositiveIntegerField(default=0)
    cancelled_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "sales summaries"

    def __str__(self):
        return f"Sales on {self.date}"


class ProductView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    session_key = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class InventoryAlert(models.Model):
    class AlertType(models.TextChoices):
        LOW_STOCK = "low_stock", "Low Stock"
        OUT_OF_STOCK = "out_of_stock", "Out of Stock"
        EXPIRING_SOON = "expiring_soon", "Expiring Soon"
        EXPIRED = "expired", "Expired"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=20, choices=AlertType.choices)
    message = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.alert_type} - {self.product.name}"
