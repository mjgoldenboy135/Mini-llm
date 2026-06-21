from django.urls import path
from .views import MCPHealthView

urlpatterns = [
    path("health/", MCPHealthView.as_view(), name="mcp_health"),
]
