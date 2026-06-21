from decimal import Decimal
import qrcode
import io, base64
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, CreateOrderSerializer
from products.models import Product


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = Order.objects.create(
            user=request.user,
            payment_method=data["payment_method"],
            delivery_type=data.get("delivery_type", "home"),
            delivery_address=data.get("delivery_address", ""),
            notes=data.get("notes", ""),
        )

        subtotal = Decimal("0.00")
        for item_data in data["items"]:
            product = Product.objects.get(id=item_data["product_id"])
            qty = int(item_data.get("qty", 1))
            OrderItem.objects.create(
                order=order, product=product, qty=qty, price=product.price
            )
            subtotal += product.price * qty

        order.subtotal = subtotal
        order.save()

        OrderStatusHistory.objects.create(
            order=order, status=Order.Status.PENDING, changed_by=request.user
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderWhatsAppView(APIView):
    """Generate QR code and WhatsApp pre-filled message for an order."""

    def get(self, request, pk):
        order = Order.objects.filter(user=request.user, id=pk).prefetch_related("items__product").first()
        if not order:
            return Response({"detail": "Not found."}, status=404)

        products_text = "\n".join(
            f"- {item.product.name} x{item.qty}" for item in order.items.all()
        )
        message = (
            f"Order Number: {order.order_number}\n\n"
            f"Products:\n{products_text}\n\n"
            "Please share delivery location."
        )
        whatsapp_url = f"https://wa.me/?text={message}"

        # generate QR
        qr = qrcode.make(whatsapp_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode()

        return Response({
            "order_number": order.order_number,
            "whatsapp_url": whatsapp_url,
            "message": message,
            "qr_code": f"data:image/png;base64,{qr_b64}",
        })
