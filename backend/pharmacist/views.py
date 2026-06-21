from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PharmacistProfile, CounsellingChecklist, ChatRequest, ChatMessage
from .serializers import (
    PharmacistProfileSerializer, CounsellingChecklistSerializer,
    ChatRequestSerializer, ChatMessageSerializer,
)
from orders.models import Order
from orders.serializers import OrderSerializer
from accounts.models import User


class IsPharmacist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (
            User.Role.PHARMACIST, User.Role.ADMIN
        )


class PharmacistDashboardView(APIView):
    permission_classes = [IsPharmacist]

    def get(self, request):
        pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
        prescription_orders = Order.objects.filter(
            prescription__status="pending"
        ).count()
        open_chats = ChatRequest.objects.filter(status=ChatRequest.Status.OPEN).count()
        active_deliveries = Order.objects.filter(
            status=Order.Status.OUT_FOR_DELIVERY
        ).count()
        return Response({
            "pending_orders": pending_orders,
            "prescription_orders": prescription_orders,
            "open_chats": open_chats,
            "active_deliveries": active_deliveries,
        })


class PharmacistOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsPharmacist]

    def get_queryset(self):
        status_filter = self.request.query_params.get("status", "pending")
        return Order.objects.filter(status=status_filter).prefetch_related("items__product")


class CounsellingView(generics.RetrieveUpdateAPIView):
    serializer_class = CounsellingChecklistSerializer
    permission_classes = [IsPharmacist]

    def get_object(self):
        order_id = self.kwargs["order_id"]
        checklist, _ = CounsellingChecklist.objects.get_or_create(
            order_id=order_id, defaults={"pharmacist": self.request.user}
        )
        return checklist


class ChatRequestListView(generics.ListAPIView):
    serializer_class = ChatRequestSerializer
    permission_classes = [IsPharmacist]

    def get_queryset(self):
        return ChatRequest.objects.filter(status=ChatRequest.Status.OPEN)


class ChatReplyView(APIView):
    permission_classes = [IsPharmacist]

    def post(self, request, chat_id):
        try:
            chat = ChatRequest.objects.get(id=chat_id)
        except ChatRequest.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        body = request.data.get("body", "")
        if not body:
            return Response({"detail": "Body required."}, status=400)
        message = ChatMessage.objects.create(chat=chat, sender=request.user, body=body)
        return Response(ChatMessageSerializer(message).data, status=201)


class StartChatView(APIView):
    """Customer opens a chat request."""

    def post(self, request):
        subject = request.data.get("subject", "")
        chat = ChatRequest.objects.create(user=request.user, subject=subject)
        return Response(ChatRequestSerializer(chat).data, status=201)
