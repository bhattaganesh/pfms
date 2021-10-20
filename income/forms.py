from django import forms
from django.forms.widgets import DateInput, NumberInput, Select, TextInput, Textarea
from .models import Income, IncomeCategory
from django.db.models import Q

class AddIncomeForm(forms.ModelForm):
    amount = forms.FloatField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your incomed amount'}), required=True)
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description about your income (optional)', 'rows': 3,'style': 'resize:none;'}), required=False)
    income_date = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    income_category = forms.ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), empty_label="Select Income Category")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddIncomeForm, self).__init__(*args, **kwargs)
        self.fields['income_category'].queryset = IncomeCategory.objects.filter(Q(created_by=user) | Q(created_by__is_admin=True)) 

    class Meta:
        model = Income
        exclude = ['entry_date', 'income_by']


class AddCateoryForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Title'}), required=True)
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description about cateogry (optional)', 'rows': 3,'style': 'resize:none;'}), required=False)
    class Meta:
        model = IncomeCategory
        exclude = ['created_by']