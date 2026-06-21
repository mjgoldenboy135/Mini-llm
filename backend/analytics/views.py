from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import SalesSummary, InventoryAlert
from orders.models import Order
from products.models import Product
from accounts.models import User


class IsAdmin(IsAuthenticated.__class__):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in (
            User.Role.ADMIN, User.Role.PHARMACIST
        )


class SalesDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        today = timezone.now().date()
        last_30 = today - timedelta(days=30)

        revenue = Order.objects.filter(
            status=Order.Status.DELIVERED,
            created_at__date__gte=last_30,
        ).aggregate(total=Sum("total"))["total"] or 0

        order_count = Order.objects.filter(created_at__date__gte=last_30).count()
        new_customers = User.objects.filter(date_joined__date__gte=last_30).count()

        top_products = (
            Order.objects.filter(status=Order.Status.DELIVERED)
            .values("items__product__name")
            .annotate(sold=Sum("items__qty"))
            .order_by("-sold")[:10]
        )

        low_stock = Product.objects.filter(stock__lte=10, is_active=True).values(
            "id", "name", "stock"
        )[:20]

        return Response({
            "period": "last_30_days",
            "revenue": revenue,
            "order_count": order_count,
            "new_customers": new_customers,
            "top_products": list(top_products),
            "low_stock_alerts": list(low_stock),
        })


class InventoryAlertListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        alerts = InventoryAlert.objects.filter(is_resolved=False).select_related("product")
        data = [
            {
                "id": str(a.id),
                "product": a.product.name,
                "alert_type": a.alert_type,
                "message": a.message,
                "created_at": a.created_at,
            }
            for a in alerts
        ]
        return Response(data)
