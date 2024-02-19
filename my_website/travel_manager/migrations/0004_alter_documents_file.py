# Generated by Django 4.2 on 2024-02-15 21:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_manager', '0003_alter_documents_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='file',
            field=models.FileField(upload_to='Media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
