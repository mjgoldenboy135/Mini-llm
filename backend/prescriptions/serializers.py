from rest_framework import serializers
from .models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            "id", "order", "patient_name", "doctor_name", "hospital_clinic",
            "upload_file", "status", "verified", "verified_by", "verified_at",
            "rejection_reason", "created_at",
        ]
        read_only_fields = ["id", "verified", "verified_by", "verified_at", "status"]


class VerifyPrescriptionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "reject"])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
