import uuid
from django.db import models
from django.conf import settings


def generate_order_number():
    from datetime import datetime
    import random
    now = datetime.now()
    return f"SP-{now.year}-{random.randint(1000, 9999)}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready for Delivery"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out for Delivery"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        MADA = "mada", "Mada"
        VISA = "visa", "Visa"
        MASTERCARD = "mastercard", "Mastercard"
        APPLE_PAY = "apple_pay", "Apple Pay"
        STC_PAY = "stc_pay", "STC Pay"
        COD = "cod", "Cash on Delivery"

    class DeliveryType(models.TextChoices):
        HOME = "home", "Home Delivery"
        PICKUP = "pickup", "Store Pickup"
        EXPRESS = "express", "Express Delivery"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    delivery_type = models.CharField(
        max_length=20, choices=DeliveryType.choices, default=DeliveryType.HOME
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    # delivery address snapshot
    delivery_address = models.TextField(blank=True)
    delivery_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    delivery_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # whatsapp QR
    whatsapp_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["order_number"]), models.Index(fields=["status"])]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
        if self.payment_method == self.PaymentMethod.COD:
            self.delivery_fee += 10  # +10 SAR COD fee
        self.total = self.subtotal + self.delivery_fee
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} x{self.qty}"

    @property
    def line_total(self):
        return self.price * self.qty


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=20, choices=Order.Status.choices)
    note = models.CharField(max_length=255, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
