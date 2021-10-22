from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms import widgets
from django.forms.widgets import DateInput, FileInput, Select, TextInput

from userInfo.models import Profile


class UserInfoUpdateForm(forms.ModelForm):
    choices = (
            (None,'__Select-Gender__'),
            ('male','Male'),
            ('female','Female')
        )
    gender = forms.ChoiceField(choices=choices, widget=Select(attrs={'class': 'form-control'}), required=False)
    birthday = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    phone = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter your phone number',}), required=False)
    # avatar = forms.ImageField(required=False)
    class Meta:
        model = Profile
        exclude = ['created_at', 'updated_at', 'user']