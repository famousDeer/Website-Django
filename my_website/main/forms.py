from django import forms
from .models import ToDoList

class CreateNewList(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['name']
    