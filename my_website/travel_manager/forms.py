from django import forms
from django_countries.fields import CountryField

class CreateNewDestination(forms.Form):
    country = CountryField().formfield(label="country")
    city = forms.CharField(label="city", max_length=100)
