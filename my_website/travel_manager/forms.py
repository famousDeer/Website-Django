from django import forms
from django_countries.fields import CountryField
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Documents, Budget, Destinations

class CreateNewDestination(forms.ModelForm):
    class Meta:
        model = Destinations
        fields = ['country', 'city']
    country = CountryField(blank_label="Select Country").formfield(label="country")

class DateForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(
            attrs={'class': 'custom-date-range'},
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
            attrs={'class': 'custom-date-range'},
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
        fields = ['file', 'description']
    description = forms.CharField(widget=forms.Textarea(attrs={"cols": "40", "rows": "5"}))

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['description', 'price']

    price = forms.FloatField(min_value=0, max_value=99999)