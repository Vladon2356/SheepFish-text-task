# Generated by Django 4.2 on 2023-09-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("check", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="check",
            name="pdf_file",
            field=models.FileField(blank=True, null=True, upload_to="pdf/"),
        ),
    ]
