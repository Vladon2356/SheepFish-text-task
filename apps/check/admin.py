from django.contrib import admin

from apps.check.models import Check


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'status', 'created_at')
    list_filter = ('printer', 'type', 'status')
