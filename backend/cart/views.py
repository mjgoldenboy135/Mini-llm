from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


class CartView(APIView):
    def _get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self._get_cart(request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        """Add or update item in cart."""
        product_id = request.data.get("product_id")
        qty = int(request.data.get("qty", 1))
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)

        cart = self._get_cart(request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            item.qty = qty
        else:
            item.qty += qty
        item.save()

        return Response(CartSerializer(cart).data)

    def delete(self, request):
        """Clear entire cart."""
        cart = self._get_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemView(APIView):
    def patch(self, request, item_id):
        """Update item quantity."""
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        qty = request.data.get("qty")
        if qty is not None:
            item.qty = int(qty)
            if item.qty <= 0:
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            item.save()
        return Response(CartSerializer(item.cart).data)

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        cart = item.cart
        item.delete()
        return Response(CartSerializer(cart).data)
