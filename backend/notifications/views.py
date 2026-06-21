from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification


class NotificationListView(generics.ListAPIView):
    from rest_framework import serializers

    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            from notifications.models import Notification
            model = Notification
            fields = ["id", "notification_type", "title", "body", "data", "is_read", "created_at"]

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkReadView(APIView):
    def post(self, request):
        ids = request.data.get("ids", [])
        if ids:
            Notification.objects.filter(user=request.user, id__in=ids).update(is_read=True)
        else:
            Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({"detail": "Marked as read."})
