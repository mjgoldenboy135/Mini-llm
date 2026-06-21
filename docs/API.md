# Safe Pharmacy API Reference

Base URL: `https://yourdomain.com/api`

Authentication: `Bearer <JWT access token>` header.

---

## Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new customer |
| POST | `/auth/login/` | Login with mobile + password |
| POST | `/auth/otp/request/` | Request OTP SMS |
| POST | `/auth/otp/verify/` | Verify OTP & get tokens |
| GET/PATCH | `/auth/me/` | Get / update current user |
| POST | `/auth/token/refresh/` | Refresh JWT access token |

---

## Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List products (search, filter) |
| GET | `/products/<id>/` | Product detail |
| GET | `/products/categories/` | All categories |

Query params: `search`, `category`, `prescription_required`, `ordering`

---

## Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart/` | View cart |
| POST | `/cart/` | Add item (`product_id`, `qty`) |
| DELETE | `/cart/` | Clear cart |
| PATCH | `/cart/items/<id>/` | Update item qty |
| DELETE | `/cart/items/<id>/` | Remove item |

---

## Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders/` | List my orders |
| POST | `/orders/create/` | Create order |
| GET | `/orders/<id>/` | Order detail |
| GET | `/orders/<id>/whatsapp/` | WhatsApp QR + pre-filled message |

### Create Order Body
```json
{
  "items": [{"product_id": "uuid", "qty": 2}],
  "payment_method": "mada|visa|mastercard|apple_pay|stc_pay|cod",
  "delivery_type": "home|pickup|express",
  "delivery_address": "string",
  "notes": "string"
}
```

---

## Prescriptions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prescriptions/` | List all (pharmacist) |
| POST | `/prescriptions/upload/` | Upload prescription |
| GET | `/prescriptions/<id>/` | Detail |
| POST | `/prescriptions/<id>/verify/` | Approve/reject (pharmacist) |

---

## AI Assistant

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/symptom/` | Start symptom check |
| POST | `/ai/session/<id>/answer/` | Submit answers, get recommendations |

### Emergency Detection Keywords
`chest pain`, `stroke`, `seizure`, `difficulty breathing`, `unconscious`, `severe bleeding`

---

## Pharmacist Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pharmacist/dashboard/` | Stats summary |
| GET | `/pharmacist/orders/` | Orders list |
| GET/PATCH | `/pharmacist/orders/<id>/counselling/` | Counselling checklist |
| GET | `/pharmacist/chats/` | Open chat requests |
| POST | `/pharmacist/chats/<id>/reply/` | Reply to chat |
| POST | `/pharmacist/chats/start/` | Customer starts chat |

---

## Family Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/family/members/` | List / create family members |
| GET/PATCH/DELETE | `/family/members/<id>/` | Detail |
| GET/POST | `/family/members/<id>/reminders/` | Medicine reminders |
| GET/PATCH/DELETE | `/family/reminders/<id>/` | Reminder detail |

---

## Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/initiate/` | Initiate payment (returns Stripe client_secret or COD confirmation) |
| POST | `/payments/webhook/` | Stripe webhook endpoint |

---

## Delivery

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/delivery/zones/` | Available delivery zones |
| GET | `/delivery/my-deliveries/` | Driver's assigned deliveries |
| PATCH | `/delivery/<id>/status/` | Update delivery status |

---

## Analytics (Admin/Pharmacist)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/dashboard/` | Sales summary (last 30 days) |
| GET | `/analytics/inventory-alerts/` | Low stock / expiry alerts |

---

## MCP Server

Run via stdio:
```bash
python backend/mcp_server/server.py
```

### Available Tools
- `search_product(query, prescription_required?)`
- `check_stock(product_id)`
- `create_order(user_id, items, payment_method, delivery_address?)`
- `verify_prescription(prescription_id, action, rejection_reason?)`
- `recommend_products(symptom)`
- `track_order(order_number)`
- `get_patient_profile(user_id)`

---

## WebSocket

Connect: `wss://yourdomain.com/ws/notifications/`
Auth: pass JWT via query string `?token=<access_token>`

Events received:
```json
{
  "type": "order_update|prescription|reminder|promotion|chat",
  "title": "string",
  "body": "string",
  "data": {}
}
```
