from django.urls import path
from .views import PrescriptionUploadView, PrescriptionDetailView, PrescriptionVerifyView, PrescriptionListView

urlpatterns = [
    path("", PrescriptionListView.as_view(), name="prescription_list"),
    path("upload/", PrescriptionUploadView.as_view(), name="prescription_upload"),
    path("<uuid:pk>/", PrescriptionDetailView.as_view(), name="prescription_detail"),
    path("<uuid:pk>/verify/", PrescriptionVerifyView.as_view(), name="prescription_verify"),
]
