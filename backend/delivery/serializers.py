from rest_framework import serializers
from .models import DeliveryZone, DeliveryAssignment


class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = ["id", "name", "fee", "is_active"]


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    driver_name = serializers.CharField(source="driver.name", read_only=True)

    class Meta:
        model = DeliveryAssignment
        fields = [
            "id", "order", "order_number", "driver", "driver_name", "zone",
            "status", "assigned_at", "picked_up_at", "delivered_at",
            "current_lat", "current_lng", "notes",
        ]
        read_only_fields = ["id", "assigned_at"]
