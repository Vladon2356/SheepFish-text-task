from django.urls import path

from apps.check.views import CheckApiView

app_name = 'check'

urlpatterns = [
    path('checks/', CheckApiView.as_view(), name='checks'),
]
