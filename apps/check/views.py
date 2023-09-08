from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.check.models import Check
from apps.check import serializers
from apps.printer.models import Printer
from apps.check.tasks import generate_pdf_for_check_task


class OrderCreateView(GenericAPIView):
    """Order create view."""
    serializer_class = serializers.OrderCreateSerializer

    def post(self, request):
        """Create an order."""
        serializer = serializers.OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        point_id = serializer.validated_data['order']['point_id']
        if Printer.objects.filter(point_id=point_id).count() == 0:
            return Response({"error": "there is no printer for this point"}, status=status.HTTP_400_BAD_REQUEST)
        order_number = serializer.validated_data['order']['order_number']
        if Check.objects.filter(order__order_number=order_number).count() > 0:
            return Response({"error": "this order already exists"}, status=status.HTTP_400_BAD_REQUEST)
        point_printer_ids = Printer.objects.filter(point_id=point_id).values_list('id', flat=True)
        for printer_id in point_printer_ids:
            new_check = Check.objects.create(printer_id=printer_id, order=serializer.validated_data['order'])
            file_name = generate_pdf_for_check_task.delay(check_id=new_check.id)
            # file_name = generate_pdf_for_check(new_check)
            new_check.pdf_file = f'pdf/{file_name}'
            new_check.status = 'rendered'
            new_check.save()
        return Response({"Message": "Checks were created"}, status=status.HTTP_201_CREATED)


class CheckApiView(GenericAPIView):
    """Check API view."""
    queryset = Check.objects.all()
    serializer_class = serializers.CheckDetailSerializer

    def get(self, request):
        """Get all checks."""
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetNonPrintedChecksByPrinter(GenericAPIView):
    serializer_class = serializers.CheckDetailSerializer

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
            checks = Check.objects.filter(printer_id=request.query_params.get('printer_id'), status='rendered')
            page = self.paginate_queryset(checks)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetPdfFile(GenericAPIView):
    serializer_class = serializers.CheckDetailSerializer

    def get(self, request, check_id):
        """Get pdf file for check by order number."""
        try:
            check = Check.objects.get(id=check_id)
        except Check.DoesNotExist:
            return Response({"error": "check not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            check.status = 'printed'
            check.save()
            return FileResponse(open(check.pdf_file.path, 'rb'), content_type='application/pdf', as_attachment=True)
        except Exception:
            return Response({"error": "file not found"}, status=status.HTTP_400_BAD_REQUEST)
