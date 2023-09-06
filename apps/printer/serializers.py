from rest_framework import serializers

from apps.printer.models import Printer


class PrinterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('id', 'name', 'api_key', 'check_type', 'point_id')
