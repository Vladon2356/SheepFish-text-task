from rest_framework import serializers

from apps.check.models import Check


class CheckDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'printer', 'type', 'order', 'status', 'pdf_file')
