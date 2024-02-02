from django import forms
from django_countries.fields import CountryField
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Documents

class CreateNewDestination(forms.Form):
    country = CountryField().formfield(label="country")
    city = forms.CharField(label="city", max_length=100)
    tiktok = forms.CharField(label="tiktok", max_length=200)

class DateForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }
        )
    )

    end_date = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            },
            range_from="start_date"
        )
    )

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['file']