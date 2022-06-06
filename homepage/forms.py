from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (CustomUser, ConsumedData)
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'birthday', 'password_hint')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'birthday', 'password_hint')


class ConsumedDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['protein'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['fat'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['carbohydrate'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})
        self.fields['vitamin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only'})

    class Meta:
        model = ConsumedData
        fields = ['username', 'protein', 'fat', 'carbohydrate', 'vitamin']
