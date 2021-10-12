from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from expense.forms import AddExpenseForm
from django.contrib import messages

from expense.models import Expense

# Create your views here.
@login_required(login_url='signin')
def index(request):
    expenses = Expense.objects.filter(expense_by=request.user)[::-1]
    return render(request, 'expense/index.html', {'expenses': expenses})


@login_required(login_url='signin')
def addExpense(request):
    form = AddExpenseForm(request.POST or None, user=request.user)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.expense_by = request.user
        expense.save()
        messages.success(request, "Expense added successfully.")
        return redirect('expenses')
    context = {'form': form}
    return render(request, 'expense/add-expense.html', context)

@login_required(login_url='signin')
def editExpense(request, id):
    expense = get_object_or_404(Expense, pk=id)
    form = AddExpenseForm(request.POST or None, instance=expense, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Expense updated successfully.")
        return redirect('expenses')
    context = {'form': form}
    return render(request, 'expense/edit-expense.html', context)