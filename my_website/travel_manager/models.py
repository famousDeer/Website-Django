from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
# Database

class Destinations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destination", null=True)
    country = CountryField()
    city = models.CharField(max_length=100)

class Information(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    fly_cost = models.FloatField()
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
class Tiktok(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

class Instagram(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

class Location_address(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icon = models.CharField(max_length=100, default="location-pin")
    marker_color = models.CharField(max_length=50, default="red")

class Planner_Date(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Planner_Descriptions(models.Model):
    planner_date = models.ForeignKey(Planner_Date, on_delete=models.CASCADE)
    date = models.DateField()
    descriptions = models.TextField()