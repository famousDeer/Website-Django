from django import forms
from django_countries.fields import CountryField

class CreateNewDestination(forms.Form):
    country = CountryField().formfield(label="country")
    city = forms.CharField(label="city", max_length=100)
    tiktok = forms.CharField(label="tiktok", max_length=200)
    instagram = forms.CharField(label="instagram", max_length=200)
