from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from orders.models import Order


class InitiatePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={"user": request.user, "amount": order.total, "method": order.payment_method},
        )

        if order.payment_method == Order.PaymentMethod.COD:
            payment.status = Payment.Status.PENDING
            payment.save()
            return Response({"payment_id": str(payment.id), "method": "cod", "status": "pending"})

        # For card payments return a Stripe PaymentIntent client_secret
        import stripe
        from django.conf import settings
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),
            currency="sar",
            metadata={"order_id": str(order.id)},
        )
        payment.gateway_reference = intent["id"]
        payment.save()
        return Response({
            "payment_id": str(payment.id),
            "client_secret": intent["client_secret"],
            "amount": str(order.total),
        })


class PaymentWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        import stripe
        from django.conf import settings
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=400)

        if event["type"] == "payment_intent.succeeded":
            intent_id = event["data"]["object"]["id"]
            Payment.objects.filter(gateway_reference=intent_id).update(
                status=Payment.Status.SUCCEEDED
            )
        elif event["type"] == "payment_intent.payment_failed":
            intent_id = event["data"]["object"]["id"]
            Payment.objects.filter(gateway_reference=intent_id).update(
                status=Payment.Status.FAILED
            )
        return Response({"status": "ok"})
