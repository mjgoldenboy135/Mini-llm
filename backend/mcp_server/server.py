"""
Safe Pharmacy MCP Server
Exposes pharmacy tools as MCP tools for AI agents.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

server = Server("safe-pharmacy")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_product",
            description="Search for pharmacy products by name, generic name, or barcode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "prescription_required": {"type": "boolean"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="check_stock",
            description="Check current stock level of a product by SKU or ID.",
            inputSchema={
                "type": "object",
                "properties": {"product_id": {"type": "string"}},
                "required": ["product_id"],
            },
        ),
        types.Tool(
            name="create_order",
            description="Create a new pharmacy order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "items": {"type": "array", "items": {"type": "object"}},
                    "payment_method": {"type": "string"},
                    "delivery_address": {"type": "string"},
                },
                "required": ["user_id", "items", "payment_method"],
            },
        ),
        types.Tool(
            name="verify_prescription",
            description="Verify a prescription by ID. Pharmacist use only.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prescription_id": {"type": "string"},
                    "action": {"type": "string", "enum": ["approve", "reject"]},
                    "rejection_reason": {"type": "string"},
                },
                "required": ["prescription_id", "action"],
            },
        ),
        types.Tool(
            name="recommend_products",
            description="Recommend OTC products for a given symptom.",
            inputSchema={
                "type": "object",
                "properties": {"symptom": {"type": "string"}},
                "required": ["symptom"],
            },
        ),
        types.Tool(
            name="track_order",
            description="Get current status and tracking info for an order.",
            inputSchema={
                "type": "object",
                "properties": {"order_number": {"type": "string"}},
                "required": ["order_number"],
            },
        ),
        types.Tool(
            name="get_patient_profile",
            description="Get a patient's profile including family members and allergies.",
            inputSchema={
                "type": "object",
                "properties": {"user_id": {"type": "string"}},
                "required": ["user_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    from products.models import Product
    from orders.models import Order
    from prescriptions.models import Prescription
    from accounts.models import User
    from family_profiles.models import FamilyMember
    from ai_assistant.views import SYMPTOM_PRODUCT_MAP

    if name == "search_product":
        query = arguments["query"]
        qs = Product.objects.filter(is_active=True).filter(
            name__icontains=query
        ) | Product.objects.filter(
            generic_name__icontains=query
        ) | Product.objects.filter(
            barcode=query
        )
        if "prescription_required" in arguments:
            qs = qs.filter(prescription_required=arguments["prescription_required"])
        results = list(qs.values("id", "name", "generic_name", "price", "stock", "prescription_required")[:10])
        return [types.TextContent(type="text", text=str(results))]

    elif name == "check_stock":
        try:
            product = Product.objects.get(id=arguments["product_id"])
            return [types.TextContent(
                type="text",
                text=f"Product: {product.name}, Stock: {product.stock}, In Stock: {product.in_stock}"
            )]
        except Product.DoesNotExist:
            return [types.TextContent(type="text", text="Product not found.")]

    elif name == "create_order":
        from django.db import transaction
        from decimal import Decimal
        try:
            user = User.objects.get(id=arguments["user_id"])
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    payment_method=arguments["payment_method"],
                    delivery_address=arguments.get("delivery_address", ""),
                )
                subtotal = Decimal("0")
                for item in arguments["items"]:
                    product = Product.objects.get(id=item["product_id"])
                    from orders.models import OrderItem
                    OrderItem.objects.create(order=order, product=product, qty=item.get("qty", 1), price=product.price)
                    subtotal += product.price * item.get("qty", 1)
                order.subtotal = subtotal
                order.save()
            return [types.TextContent(type="text", text=f"Order created: {order.order_number}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "verify_prescription":
        from django.utils import timezone
        try:
            rx = Prescription.objects.get(id=arguments["prescription_id"])
            if arguments["action"] == "approve":
                rx.verified = True
                rx.status = Prescription.Status.VERIFIED
                rx.verified_at = timezone.now()
            else:
                rx.status = Prescription.Status.REJECTED
                rx.rejection_reason = arguments.get("rejection_reason", "")
            rx.save()
            return [types.TextContent(type="text", text=f"Prescription {rx.id} {arguments['action']}d.")]
        except Prescription.DoesNotExist:
            return [types.TextContent(type="text", text="Prescription not found.")]

    elif name == "recommend_products":
        symptom = arguments["symptom"].lower()
        product_names = []
        for key, names in SYMPTOM_PRODUCT_MAP.items():
            if key in symptom:
                product_names = names
                break
        products = list(Product.objects.filter(
            name__in=product_names, is_active=True, prescription_required=False
        ).values("id", "name", "price"))
        return [types.TextContent(type="text", text=str(products))]

    elif name == "track_order":
        try:
            order = Order.objects.get(order_number=arguments["order_number"])
            history = list(order.status_history.values("status", "note", "created_at"))
            return [types.TextContent(
                type="text",
                text=f"Order {order.order_number}: {order.status}\nHistory: {history}"
            )]
        except Order.DoesNotExist:
            return [types.TextContent(type="text", text="Order not found.")]

    elif name == "get_patient_profile":
        try:
            user = User.objects.get(id=arguments["user_id"])
            members = list(FamilyMember.objects.filter(user=user).values(
                "name", "relationship", "allergies", "medical_conditions", "current_medicines"
            ))
            return [types.TextContent(
                type="text",
                text=f"Patient: {user.name} ({user.mobile})\nFamily: {members}"
            )]
        except User.DoesNotExist:
            return [types.TextContent(type="text", text="User not found.")]

    return [types.TextContent(type="text", text="Unknown tool.")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
