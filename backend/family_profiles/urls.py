from django.urls import path
from .views import (
    FamilyMemberListCreateView, FamilyMemberDetailView,
    MedicineReminderListCreateView, MedicineReminderDetailView,
)

urlpatterns = [
    path("members/", FamilyMemberListCreateView.as_view(), name="family_member_list"),
    path("members/<uuid:pk>/", FamilyMemberDetailView.as_view(), name="family_member_detail"),
    path("members/<uuid:member_id>/reminders/", MedicineReminderListCreateView.as_view(), name="reminder_list"),
    path("reminders/<uuid:pk>/", MedicineReminderDetailView.as_view(), name="reminder_detail"),
]
