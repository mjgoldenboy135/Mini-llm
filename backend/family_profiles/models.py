import uuid
from django.db import models
from django.conf import settings


class FamilyMember(models.Model):
    class Relationship(models.TextChoices):
        SELF = "self", "Self"
        SPOUSE = "spouse", "Spouse"
        CHILD = "child", "Child"
        PARENT = "parent", "Parent"
        SIBLING = "sibling", "Sibling"
        OTHER = "other", "Other"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="family_members"
    )
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=20, choices=Relationship.choices)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    current_medicines = models.TextField(blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_relationship_display()}) of {self.user.name}"


class MedicineReminder(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        TWICE_DAILY = "twice_daily", "Twice Daily"
        THREE_TIMES = "three_times", "Three Times Daily"
        WEEKLY = "weekly", "Weekly"
        AS_NEEDED = "as_needed", "As Needed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    family_member = models.ForeignKey(
        FamilyMember, on_delete=models.CASCADE, related_name="reminders"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    medicine_name = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reminder_times = models.JSONField(default=list)  # ["08:00", "20:00"]
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["medicine_name"]

    def __str__(self):
        return f"{self.medicine_name} for {self.family_member.name}"
