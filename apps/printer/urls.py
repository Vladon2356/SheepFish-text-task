from django.urls import path

from apps.printer.views import PrinterApiView

app_name = 'printer'

urlpatterns = [
    path('printers/', PrinterApiView.as_view(), name='printers'),
]
