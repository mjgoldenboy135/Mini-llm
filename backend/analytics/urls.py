from django.urls import path
from .views import SalesDashboardView, InventoryAlertListView

urlpatterns = [
    path("dashboard/", SalesDashboardView.as_view(), name="analytics_dashboard"),
    path("inventory-alerts/", InventoryAlertListView.as_view(), name="inventory_alerts"),
]
