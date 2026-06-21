from rest_framework import serializers
from .models import FamilyMember, MedicineReminder


class MedicineReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineReminder
        fields = [
            "id", "family_member", "product", "medicine_name", "dose",
            "frequency", "start_date", "end_date", "reminder_times", "is_active", "notes",
        ]
        read_only_fields = ["id"]


class FamilyMemberSerializer(serializers.ModelSerializer):
    reminders = MedicineReminderSerializer(many=True, read_only=True)

    class Meta:
        model = FamilyMember
        fields = [
            "id", "name", "relationship", "dob", "gender",
            "allergies", "medical_conditions", "current_medicines", "reminders",
        ]
        read_only_fields = ["id"]
