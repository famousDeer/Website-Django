from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField


# Create your models here.
# Database

class Destinations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destination", null=True)
    country = CountryField()
    city = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Information(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    fly_cost = models.FloatField()
    description = models.TextField()
    
class Tiktok(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    link = models.CharField(max_length=256)

class Location_address(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icon = models.CharField(max_length=128, default="location-pin")
    marker_color = models.CharField(max_length=64, default="red")
    inside_planner = models.BooleanField(default=False)
    descriptions = models.TextField(default='Attration')
    price = models.FloatField(default=0)

class Planner_Date(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Planner_Table_Date(models.Model):
    planner_date = models.ForeignKey(Planner_Date, on_delete=models.CASCADE)
    date = models.DateField(primary_key=True)

class Planner_Table_Descriptions(models.Model):
    planner_table_date = models.ForeignKey(Planner_Table_Date, on_delete=models.CASCADE)
    location_address = models.ForeignKey(Location_address, on_delete=models.CASCADE)
    descriptions = models.TextField()
    color_label = models.TextField()

class Documents(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    file = models.FileField(upload_to="Media/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    