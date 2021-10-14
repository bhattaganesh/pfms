from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from expense.forms import AddExpenseForm, AddCateoryForm
from django.contrib import messages
from django.db.models import Q

from expense.models import Expense, ExpenseCategory
from currency.models import Currency

# Create your views here.
@login_required(login_url='signin')
def index(request):
    expenses = Expense.objects.filter(expense_by=request.user)[::-1]
    if Currency.objects.filter(user=request.user).exists():
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    else:
        currency = 'NPR'
    return render(request, 'expense/index.html', {'expenses': expenses, 'currency': currency})


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

@login_required(login_url='signin')
def viewExpense(request, id):
    expense = get_object_or_404(Expense, pk=id)
    context = {'expense': expense}
    return render(request, 'expense/expense-details.html', context)

@login_required(login_url='signin')
def deleteExpense(request, id):
    expense = get_object_or_404(Expense, pk=id)
    if request.method =="POST":
        expense.delete()
        messages.success(request, "Expense Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='signin')
def listAllCategories(request):
    categories = ExpenseCategory.objects.filter(Q(created_by=request.user) | Q(created_by=1))[::-1]
    return render(request, 'expense-category/index.html', {'categories': categories})


@login_required(login_url='signin')
def addCategory(request):
    form = AddCateoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.created_by = request.user
        category.save()
        messages.success(request, "Expense category added successfully.")
        return redirect('expense-categories')
    context = {'form': form}
    return render(request, 'expense-category/add-expense-category.html', context)

@login_required(login_url='signin')
def editCategory(request, id):
    category = get_object_or_404(ExpenseCategory, pk=id)
    form = AddCateoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Expense Category updated successfully.")
        return redirect('expense-categories')
    context = {'form': form}
    return render(request, 'expense-category/edit-expense-category.html', context)

@login_required(login_url='signin')
def viewCategory(request, id):
    category = get_object_or_404(ExpenseCategory, pk=id)
    context = {'category': category}
    return render(request, 'expense-category/expense-category-details.html', context)

@login_required(login_url='signin')
def deleteCategory(request, id):
    category = get_object_or_404(ExpenseCategory, pk=id)
    if request.method =="POST":
        category.delete()
        messages.success(request, "Expense Category Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))