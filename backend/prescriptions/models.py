import uuid
from django.db import models
from django.conf import settings


class Prescription(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending Review"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="prescription"
    )
    patient_name = models.CharField(max_length=150)
    doctor_name = models.CharField(max_length=150, blank=True)
    hospital_clinic = models.CharField(max_length=150, blank=True)
    upload_file = models.FileField(upload_to="prescriptions/")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_prescriptions",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rx for {self.order.order_number} - {self.patient_name}"
