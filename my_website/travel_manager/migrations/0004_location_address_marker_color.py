# Generated by Django 4.2 on 2024-01-28 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_manager', '0003_location_address_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='location_address',
            name='marker_color',
            field=models.CharField(default='red', max_length=50),
        ),
    ]