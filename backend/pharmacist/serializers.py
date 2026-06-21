from rest_framework import serializers
from .models import PharmacistProfile, CounsellingChecklist, ChatRequest, ChatMessage


class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = ["id", "license_number", "license_expiry", "is_on_duty"]


class CounsellingChecklistSerializer(serializers.ModelSerializer):
    is_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = CounsellingChecklist
        fields = [
            "id", "order", "pharmacist", "indication_explained", "dose_explained",
            "duration_explained", "storage_explained", "side_effects_explained",
            "notes", "is_complete", "completed_at",
        ]
        read_only_fields = ["id", "pharmacist", "completed_at"]


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "sender_name", "body", "created_at"]
        read_only_fields = ["id", "sender", "created_at"]


class ChatRequestSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRequest
        fields = ["id", "user", "pharmacist", "status", "subject", "messages", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
