# Generated by Django 4.2 on 2024-01-27 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('destinations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_manager.destinations')),
            ],
        ),
    ]
