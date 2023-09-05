from django.contrib import admin


from apps.printer.models import Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'check_type', 'point_id')
    list_filter = ('check_type', 'point_id')
