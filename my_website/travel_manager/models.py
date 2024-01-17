from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
# Database

class Destinations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destination", null=True)
    country = CountryField()
    city = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.city

class Information(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    fly_cost = models.FloatField()
    description = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.description
    
class Tiktok(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)

class Instagram(models.Model):
    destinations = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)