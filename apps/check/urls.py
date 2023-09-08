from django.urls import path

from apps.check import views

app_name = 'check'

urlpatterns = [
    path('order/', views.OrderCreateView.as_view(), name='order_create'),

    path('checks/', views.CheckApiView.as_view(), name='checks'),
    path('checks/by-printer/', views.GetNonPrintedChecksByPrinter.as_view(), name='checks_by_printer'),
    path('checks/download-pdf/<int:check_id>/', views.GetPdfFile.as_view(), name='checks_download_pdf'),
]
