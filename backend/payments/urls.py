from django.urls import path
from .views import InitiatePaymentView, PaymentWebhookView

urlpatterns = [
    path("initiate/", InitiatePaymentView.as_view(), name="payment_initiate"),
    path("webhook/", PaymentWebhookView.as_view(), name="payment_webhook"),
]
