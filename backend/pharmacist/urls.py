from django.urls import path
from .views import (
    PharmacistDashboardView, PharmacistOrderListView, CounsellingView,
    ChatRequestListView, ChatReplyView, StartChatView,
)

urlpatterns = [
    path("dashboard/", PharmacistDashboardView.as_view(), name="pharmacist_dashboard"),
    path("orders/", PharmacistOrderListView.as_view(), name="pharmacist_orders"),
    path("orders/<uuid:order_id>/counselling/", CounsellingView.as_view(), name="counselling"),
    path("chats/", ChatRequestListView.as_view(), name="chat_list"),
    path("chats/<uuid:chat_id>/reply/", ChatReplyView.as_view(), name="chat_reply"),
    path("chats/start/", StartChatView.as_view(), name="chat_start"),
]
