from django.urls import path
from .views import DeliveryZoneListView, DriverDeliveryListView, UpdateDeliveryStatusView

urlpatterns = [
    path("zones/", DeliveryZoneListView.as_view(), name="delivery_zones"),
    path("my-deliveries/", DriverDeliveryListView.as_view(), name="driver_deliveries"),
    path("<uuid:pk>/status/", UpdateDeliveryStatusView.as_view(), name="delivery_status_update"),
]
