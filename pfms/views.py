from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from expense.models import Expense
from income.models import Income
from currency.models import Currency
from functools import reduce
@login_required(login_url='signin')
def index(request):
    expense_count = 0
    income_count = 0
    total_income = 0
    total_expense = 0
    expenses = Expense.objects.filter(expense_by=request.user)
    incomes = Income.objects.filter(income_by=request.user)
    expense_count = expenses.count()
    income_count = incomes.count()

    # total_expense = sum(expenses.values_list('amount', flat=True))
    # def add_amount(a, b):
    #     return a+b
    # total_expense = reduce(add_amount, expenses.values_list('amount', flat=True))
    if expense_count:
        total_expense = reduce(lambda a, b : a + b, expenses.values_list('amount', flat=True))
    # import pdb; pdb.set_trace()
    if income_count:
        total_income = sum(incomes.values_list('amount', flat=True))

    profit = total_income - total_expense

    if profit >= 0:
        profit_or_loss = ['Profit', profit]
    else:
        profit_or_loss = ['Loss', abs(profit)]

    try:
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    except:
        currency = "Choose Currency"


    context = {
        'expense_count': expense_count,
        'income_count': income_count,
        'total_expense': total_expense,
        'total_income': total_income,
        'profit_or_loss_key': profit_or_loss[0],
        'profit_or_loss_val': profit_or_loss[1],
        'currency': currency,
    }

    return render(request, 'dashboard/dashboard.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('signin')

