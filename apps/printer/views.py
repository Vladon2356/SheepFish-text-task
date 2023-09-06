from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from apps.printer.models import Printer
from apps.printer.serializers import PrinterDetailSerializer


class PrinterApiView(GenericAPIView):
    """Check API view."""
    serializer_class = PrinterDetailSerializer

    def get(self, request):
        """Get all checks."""
        checks = Printer.objects.all()
        data = PrinterDetailSerializer(checks, many=True).data
        return Response(data)

    def post(self, request):
        """Create a check."""
        serializer = PrinterDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)
