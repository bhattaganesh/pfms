from django import forms
from django.forms.widgets import DateInput, NumberInput, Select, TextInput, Textarea
from django.http import request
from .models import Expense, ExpenseCategory
from django.db.models import Q

class AddExpenseForm(forms.ModelForm):
    amount = forms.FloatField(widget=NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your expensed amount'}), required=True)
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description about your expense (optional)', 'rows': 3,'style': 'resize:none;'}), required=False)
    expense_date = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    expense_category = forms.ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'form-control'}), empty_label="Select Expense Category")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        # self.fields['expense_category'].queryset = ExpenseCategory.objects.filter(created_by=user) | ExpenseCategory.objects.filter(created_by=1)
        self.fields['expense_category'].queryset = ExpenseCategory.objects.filter(Q(created_by=user) | Q(created_by=1)) 

    class Meta:
        model = Expense
        exclude = ['entry_date', 'expense_by']


class AddCateoryForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Title'}), required=True)
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description about cateogry (optional)', 'rows': 3,'style': 'resize:none;'}), required=False)
    class Meta:
        model = ExpenseCategory
        exclude = ['created_by']