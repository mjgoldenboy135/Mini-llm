from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prescription
from .serializers import PrescriptionSerializer, VerifyPrescriptionSerializer
from accounts.models import User


class PrescriptionUploadView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer

    def perform_create(self, serializer):
        serializer.save()


class PrescriptionDetailView(generics.RetrieveAPIView):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        return Prescription.objects.filter(order__user=self.request.user)


class PrescriptionVerifyView(APIView):
    """Pharmacist endpoint to approve or reject a prescription."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role not in (User.Role.PHARMACIST, User.Role.ADMIN):
            return Response({"detail": "Forbidden."}, status=403)
        try:
            rx = Prescription.objects.get(id=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        serializer = VerifyPrescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data["action"]

        if action == "approve":
            rx.verified = True
            rx.status = Prescription.Status.VERIFIED
            rx.verified_by = request.user
            rx.verified_at = timezone.now()
        else:
            rx.status = Prescription.Status.REJECTED
            rx.rejection_reason = serializer.validated_data.get("rejection_reason", "")

        rx.save()
        return Response(PrescriptionSerializer(rx).data)


class PrescriptionListView(generics.ListAPIView):
    """Pharmacist sees all pending prescriptions."""
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Prescription.objects.all().select_related("order__user")
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs
