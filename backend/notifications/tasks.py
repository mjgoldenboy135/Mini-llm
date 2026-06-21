from config.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


@app.task
def send_notification(user_id: str, notification_type: str, title: str, body: str, data: dict = None):
    from accounts.models import User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    notif = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        body=body,
        data=data or {},
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            "type": "notification_message",
            "data": {
                "id": str(notif.id),
                "type": notification_type,
                "title": title,
                "body": body,
                "data": data or {},
            },
        },
    )


@app.task
def send_whatsapp_order_confirmation(order_id: str):
    from orders.models import Order
    from django.conf import settings
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    if not settings.TWILIO_ACCOUNT_SID:
        return

    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    products_text = "\n".join(
        f"- {item.product.name} x{item.qty}" for item in order.items.all()
    )
    message_body = (
        f"Order Number: {order.order_number}\n\n"
        f"Products:\n{products_text}\n\n"
        "Please share your delivery location."
    )

    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        body=message_body,
        to=f"whatsapp:{order.user.mobile}",
    )

    order.whatsapp_sent = True
    order.save(update_fields=["whatsapp_sent"])
