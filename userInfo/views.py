from django.shortcuts import render
from django.http import JsonResponse
from currency.models import Currency
from expense.models import Expense
from income.models import Income
from userInfo.forms import UserInfoUpdateForm
from userInfo.models import Profile
from authentication.models import User
from functools import reduce
import os
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def userInfo(request):
    avatar = ''
    try:
        user_info = Profile.objects.get(user=request.user)
        if len(request.user.user_profile.avatar.name):
            avatar= request.user.user_profile.avatar.path
        # import pdb; pdb.set_trace()
        form = UserInfoUpdateForm(request.POST or None, request.FILES or None, instance=user_info)
    except:
        form = UserInfoUpdateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            name = request.POST.get('name')
            if name == '':
                form.errors.update({'name': 'Name can\'t be empty. '})
                return JsonResponse({'status': False, 'errors': form.errors})

            if len(name) < 3:
                form.errors.update({'name': 'Name should have at least length  3.'})
                return JsonResponse({'status': False, 'errors': form.errors})

            if name != request.user.name:
                user = User.objects.get(id=request.user.id)
                user.name = name
                user.save()
            
            # import pdb; pdb.set_trace()

            if request.FILES:
                if len(avatar):
                    os.remove(avatar)

            profile.save()
            return JsonResponse({'status': True, 'msg': 'Updated Successfully.'})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        # form = UserInfoUpdateForm()


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
            'form': form
        }

        return render(request, 'profile/profile.html', context)