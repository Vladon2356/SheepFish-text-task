from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from apps.check.models import Check
from apps.check.serializers import CheckDetailSerializer


class CheckApiView(GenericAPIView):
    """Check API view."""
    serializer_class = CheckDetailSerializer

    def get(self, request):
        """Get all checks."""
        checks = Check.objects.all()
        data = CheckDetailSerializer(checks, many=True).data
        return Response(data)

    def post(self, request):
        """Create a check."""
        serializer = CheckDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)
