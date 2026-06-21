import uuid
from django.db import models
from django.conf import settings


class PharmacistProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pharmacist_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    is_on_duty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pharmacist: {self.user.name}"


class CounsellingChecklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="counselling"
    )
    pharmacist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    indication_explained = models.BooleanField(default=False)
    dose_explained = models.BooleanField(default=False)
    duration_explained = models.BooleanField(default=False)
    storage_explained = models.BooleanField(default=False)
    side_effects_explained = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_complete(self):
        return all(
            [
                self.indication_explained,
                self.dose_explained,
                self.duration_explained,
                self.storage_explained,
                self.side_effects_explained,
            ]
        )

    def __str__(self):
        return f"Counselling for {self.order.order_number}"


class ChatRequest(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        ASSIGNED = "assigned", "Assigned"
        CLOSED = "closed", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_requests"
    )
    pharmacist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_chats",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    subject = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Chat #{self.id} - {self.user.name}"


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(ChatRequest, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
