from django.db import models


class Printer(models.Model):
    class CheckTypeChoices(models.TextChoices):
        CLIENT = 'client', 'Client'
        KITCHEN = 'kitchen', 'Kitchen'

    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    check_type = models.CharField(max_length=10, choices=CheckTypeChoices.choices)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Printers'
        verbose_name = 'Printer'
        ordering = ['name']
