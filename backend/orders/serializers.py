from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "qty", "price", "line_total"]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["status", "note", "created_at"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "payment_method", "delivery_type",
            "subtotal", "delivery_fee", "total", "notes", "delivery_address",
            "delivery_lat", "delivery_lng", "items", "status_history",
            "whatsapp_sent", "created_at",
        ]
        read_only_fields = ["id", "order_number", "subtotal", "delivery_fee", "total"]


class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
    )
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)
    delivery_type = serializers.ChoiceField(choices=Order.DeliveryType.choices, default="home")
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
