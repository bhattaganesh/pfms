from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from income.forms import AddIncomeForm, AddCateoryForm
from django.contrib import messages
from django.db.models import Q
from income.models import Income, IncomeCategory
from django.core.paginator import Paginator
from currency.models import Currency

# Create your views here.
@login_required(login_url='signin')
def index(request):
    incomes = Income.objects.filter(income_by=request.user)[::-1]
    if Currency.objects.filter(user=request.user).exists():
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    else:
        currency = 'NPR'

    return render(request, 'income/index.html', {'incomes': incomes, 'currency': currency})


@login_required(login_url='signin')
def addIncome(request):
    form = AddIncomeForm(request.POST or None, user=request.user)
    if form.is_valid():
        income = form.save(commit=False)
        income.income_by = request.user
        income.save()
        messages.success(request, "Income added successfully.")
        return redirect('incomes')
    context = {'form': form}
    return render(request, 'income/add-income.html', context)

@login_required(login_url='signin')
def editIncome(request, id):
    income = get_object_or_404(Income, pk=id)
    form = AddIncomeForm(request.POST or None, instance=income, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Income updated successfully.")
        return redirect('incomes')
    context = {'form': form}
    return render(request, 'income/edit-income.html', context)

@login_required(login_url='signin')
def viewIncome(request, id):
    income = get_object_or_404(Income, pk=id)
    context = {'income': income}
    return render(request, 'income/income-details.html', context)

@login_required(login_url='signin')
def deleteIncome(request, id):
    income = get_object_or_404(Income, pk=id)
    if request.method =="POST":
        income.delete()
        messages.success(request, "Income Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='signin')
def listAllCategories(request):
    categories = IncomeCategory.objects.filter(Q(created_by=request.user) | Q(created_by=1))[::-1]
    paginator = Paginator(categories, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    return render(request, 'income-category/index.html', {
        'categories': categories,
        'page_obj': page_obj
        }) 


@login_required(login_url='signin')
def addCategory(request):
    form = AddCateoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.created_by = request.user
        category.save()
        messages.success(request, "Income category added successfully.")
        return redirect('income-categories')
    context = {'form': form}
    return render(request, 'income-category/add-income-category.html', context)

@login_required(login_url='signin')
def editCategory(request, id):
    category = get_object_or_404(IncomeCategory, pk=id)
    form = AddCateoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Income Category updated successfully.")
        return redirect('income-categories')
    context = {'form': form}
    return render(request, 'income-category/edit-income-category.html', context)

@login_required(login_url='signin')
def viewCategory(request, id):
    category = get_object_or_404(IncomeCategory, pk=id)
    context = {'category': category}
    return render(request, 'income-category/income-category-details.html', context)

@login_required(login_url='signin')
def deleteCategory(request, id):
    category = get_object_or_404(IncomeCategory, pk=id)
    if request.method =="POST":
        category.delete()
        messages.success(request, "Income Category Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))