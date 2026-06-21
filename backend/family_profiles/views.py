from rest_framework import generics
from .models import FamilyMember, MedicineReminder
from .serializers import FamilyMemberSerializer, MedicineReminderSerializer


class FamilyMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = FamilyMemberSerializer

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FamilyMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FamilyMemberSerializer

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)


class MedicineReminderListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicineReminderSerializer

    def get_queryset(self):
        member_id = self.kwargs.get("member_id")
        return MedicineReminder.objects.filter(
            family_member_id=member_id, family_member__user=self.request.user
        )


class MedicineReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicineReminderSerializer

    def get_queryset(self):
        return MedicineReminder.objects.filter(family_member__user=self.request.user)
