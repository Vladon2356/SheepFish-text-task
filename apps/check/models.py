from django.db import models

from apps.printer.models import Printer


class Check(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'new', 'new'
        RENDERED = 'rendered', 'rendered'
        PRINTED = 'printed', 'printed'

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    order = models.JSONField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.NEW)
    pdf_file = models.FileField(upload_to='pdf/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'check #{self.id} {self.type}'

    def save(self, *args, **kwargs):
        self.type = self.printer.check_type
        super().save()

    class Meta:
        verbose_name_plural = 'Checks'
        verbose_name = 'Check'
        ordering = ['-created_at']
