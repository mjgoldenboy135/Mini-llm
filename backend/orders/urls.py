from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView, OrderWhatsAppView

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", CreateOrderView.as_view(), name="order_create"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("<uuid:pk>/whatsapp/", OrderWhatsAppView.as_view(), name="order_whatsapp"),
]
