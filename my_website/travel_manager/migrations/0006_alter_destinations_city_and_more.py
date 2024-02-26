# Generated by Django 4.2 on 2024-02-18 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_manager', '0005_alter_location_address_descriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinations',
            name='city',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='location_address',
            name='address',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='location_address',
            name='icon',
            field=models.CharField(default='location-pin', max_length=128),
        ),
        migrations.AlterField(
            model_name='location_address',
            name='marker_color',
            field=models.CharField(default='red', max_length=64),
        ),
        migrations.AlterField(
            model_name='tiktok',
            name='link',
            field=models.CharField(max_length=256),
        ),
    ]