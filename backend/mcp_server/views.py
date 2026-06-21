from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser


class MCPHealthView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"status": "MCP server is configured. Run via stdio."})
