from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.check.models import Check
from apps.check.serializers import CheckDetailSerializer, CheckCreateSerializer
from apps.check.services import generate_pdf_for_check
from apps.printer.models import Printer
from apps.check.tasks import generate_pdf_for_check_task


class CheckApiView(GenericAPIView):
    """Check API view."""
    serializer_class = CheckDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CheckCreateSerializer
        return CheckDetailSerializer

    def get(self, request):
        """Get all checks."""
        checks = Check.objects.all()
        data = CheckDetailSerializer(checks, many=True).data
        return Response(data)

    def post(self, request):
        """Create a check."""
        serializer = CheckCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        point_id = serializer.validated_data['order']['point_id']
        if Printer.objects.filter(point_id=point_id).count() == 0:
            return Response({"error": "no printer for this point"}, status=status.HTTP_400_BAD_REQUEST)
        order_number = serializer.validated_data['order']['order_number']
        if Check.objects.filter(order__order_number=order_number).count() > 0:
            return Response({"error": "this order already exists"}, status=status.HTTP_400_BAD_REQUEST)
        point_printer_ids = Printer.objects.filter(point_id=point_id).values_list('id', flat=True)
        for printer_id in point_printer_ids:
            serializer.save(printer_id=printer_id)
            generate_pdf_for_check_task.delay(serializer.data)
        return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)


class GetNonPrintedChecksByPrinter(GenericAPIView):
    serializer_class = CheckDetailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'printer_id',
                openapi.IN_QUERY,
                description='Printer id',
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request):
        """Get all non-printed checks for printer by id."""
        if request.query_params.get('printer_id'):
            checks = Check.objects.filter(printer_id=request.query_params.get('printer_id'), check__status='rendered')
            data = CheckDetailSerializer(checks, many=True).data
            for item in checks:
                item.status = 'printed'
                item.save()
            return Response(data)


class GetPdfFile(GenericAPIView):
    serializer_class = CheckDetailSerializer

    def get(self, request, order_number):
        """Get pdf file for check by order number."""
        try:
            check = Check.objects.get(order__order_number=order_number)
        except Check.DoesNotExist:
            return Response({"error": "check not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return FileResponse(open(check.pdf_file.path, 'rb'), content_type='application/pdf', as_attachment=True)
        except Exception:
            return Response({"error": "file not found"}, status=status.HTTP_400_BAD_REQUEST)
