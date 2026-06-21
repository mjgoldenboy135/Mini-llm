from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryZone, DeliveryAssignment
from .serializers import DeliveryZoneSerializer, DeliveryAssignmentSerializer
from accounts.models import User


class DeliveryZoneListView(generics.ListAPIView):
    queryset = DeliveryZone.objects.filter(is_active=True)
    serializer_class = DeliveryZoneSerializer


class DriverDeliveryListView(generics.ListAPIView):
    serializer_class = DeliveryAssignmentSerializer

    def get_queryset(self):
        return DeliveryAssignment.objects.filter(driver=self.request.user).select_related("order")


class UpdateDeliveryStatusView(APIView):
    def patch(self, request, pk):
        try:
            assignment = DeliveryAssignment.objects.get(id=pk, driver=request.user)
        except DeliveryAssignment.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        new_status = request.data.get("status")
        if new_status not in DeliveryAssignment.Status.values:
            return Response({"detail": "Invalid status."}, status=400)

        assignment.status = new_status
        if new_status == DeliveryAssignment.Status.PICKED_UP:
            assignment.picked_up_at = timezone.now()
        elif new_status == DeliveryAssignment.Status.DELIVERED:
            assignment.delivered_at = timezone.now()

        lat = request.data.get("lat")
        lng = request.data.get("lng")
        if lat:
            assignment.current_lat = lat
        if lng:
            assignment.current_lng = lng

        assignment.save()
        return Response(DeliveryAssignmentSerializer(assignment).data)
