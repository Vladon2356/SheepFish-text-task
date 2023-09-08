from django.db import models


class Printer(models.Model):
    class PrinterCheckTypeChoices(models.TextChoices):
        CLIENT = 'client', 'client'
        KITCHEN = 'kitchen', 'kitchen'

    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    check_type = models.CharField(max_length=10, choices=PrinterCheckTypeChoices.choices)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Printers'
        verbose_name = 'Printer'
        ordering = ['name']
