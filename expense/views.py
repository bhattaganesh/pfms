import pdb
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from expense.forms import AddExpenseForm, AddCateoryForm
from django.contrib import messages
from django.db.models import Q
import datetime as dt
from expense.models import Expense, ExpenseCategory
from currency.models import Currency
import json
from django.core.paginator import Paginator


# Create your views here.
@login_required(login_url='signin')
def index(request):
    expenses = Expense.objects.filter(expense_by=request.user).order_by('-id')
    if Currency.objects.filter(user=request.user).exists():
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    else:
        messages.info(request, "Please, choose your prefered currency.")
        return redirect('currency')

    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'expense/index.html', {
        'currency': currency,
        'page_obj': page_obj
        })

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
def deleteExpenses(request):
    if request.method =="POST":
        ids = list(map(lambda id:int(id), request.POST['ids'].split(",")))

        def deleteRecord(id):
            # import pdb; pdb.set_trace()
            return get_object_or_404(Expense, pk=id).delete()
        ids = list(map(deleteRecord, list(ids)))

        # import pdb; pdb.set_trace()
        messages.success(request, "Expense Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))


###################################################################################  for expense category


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

@login_required(login_url='signin')
def deleteCategories(request):
    if request.method =="POST":
        ids = list(map(lambda id:int(id), request.POST['ids'].split(",")))
        # import pdb; pdb.set_trace()

        def deleteRecord(id):
            # import pdb; pdb.set_trace()
            category = get_object_or_404(ExpenseCategory, pk=id)
            category.delete()

        ids = list(map(deleteRecord, list(ids)))

        messages.success(request, "Expense Category Deleted successfully.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))

###################################################################################  for expense summary

@login_required(login_url='signin')
def expenseSummaryByCategory(request):
    todays_date = dt.date.today()
    day = int(request.GET['day'])
    # import pdb; pdb.set_trace()
    six_month_ago = todays_date - dt.timedelta(days=day)
    expenses = Expense.objects.filter(expense_by=request.user, entry_date__gte=six_month_ago, entry_date__lte=todays_date)
    finalrep = {}


    def get_category(expense):
        # import pdb; pdb.set_trace()
        return expense.expense_category
    
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(expense_category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y.title] = get_expense_category_amount(y)
    # import pdb; pdb.set_trace()
    return JsonResponse({'category_data': finalrep}, safe=False)

def expenseSummary(request):
    if not Currency.objects.filter(user=request.user).exists():
        messages.info(request, "Please, choose your prefered currency.")
        return redirect('currency')

    expenses = Expense.objects.filter(expense_by=request.user)
    todays_amount = 0
    todays_count = 0
    this_weeks_amount = 0
    this_weeks_count = 0
    this_months_amount = 0
    this_months_count = 0
    this_years_amount = 0
    this_years_count = 0
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=7)
    month_ago = today - dt.timedelta(days=30)
    year_ago = today - dt.timedelta(days=366)
    for expense in expenses:
        if expense.entry_date == today:
            todays_amount += expense.amount
            todays_count += 1
            
        if expense.entry_date >= week_ago:
            this_weeks_amount += expense.amount
            this_weeks_count += 1

        if expense.entry_date >= month_ago:
            this_months_amount += expense.amount
            this_months_count += 1

        if expense.entry_date >= year_ago:
            this_years_amount += expense.amount
            this_years_count += 1
    currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    context = {
        'today': {
            'todays_amount': todays_amount,
            'todays_count': todays_count
        },
        'week': {
            'this_weeks_amount': this_weeks_amount,
            'this_weeks_count': this_weeks_count
        },
        'month': {
            'this_months_amount': this_months_amount,
            'this_months_count': this_months_count
        },
        'year': {
            'this_years_amount': this_years_amount,
            'this_years_count': this_years_count
        },
        'currency': currency
    }
    # import pdb; pdb.set_trace()
    return render(request, 'expense/expense-summary.html', context)



def monthlyWiseExpense(request):
    today = dt.date.today()
    six_month_ago = today - dt.timedelta(days=180)
    expenses = Expense.objects.filter(expense_by=request.user, entry_date__gte=six_month_ago, entry_date__lte=today)
    months = []
    for expense in expenses:
        print(expense)
        # month = dt.date(2021, 2, 5).month
        # dateformat = expense.entry_date.strftime("%Y, %m, %d")
        month = expense.entry_date.strftime("%m")
        months.append(month)
    # import pdb; pdb.set_trace()
    months = list(set(months))
    return HttpResponse(months)




# def income_summary_rest(request):
#     all_income = Expense.objects.filter(owner=request.user)
#     today = dt.datetime.today().date()
#     today_amount = 0
#     months_data = {}
#     week_days_data = {}

#     def get_amount_for_month(month):
#         month_amount = 0
#         for one in all_income:
#             month_, year = one.income_date.month, one.income_date.year
#             if month == month_ and year == today_year:
#                 month_amount += one.amount
#         return month_amount

#     for x in range(1, 13):
#         today_month, today_year = x, dt.datetime.today().year
#         for one in all_income:
#             months_data[x] = get_amount_for_month(x)

#     def get_amount_for_day(x, today_day, month, today_year):
#         day_amount = 0
#         for one in all_income:
#             day_, date_,  month_, year_ = one.income_date.isoweekday(
#             ), one.income_date.day, one.income_date.month, one.income_date.year
#             if x == day_ and month == month_ and year_ == today_year:
#                 if not day_ > today_day:
#                     day_amount += one.amount
#         return day_amount

#     for x in range(1, 8):
#         today_day, today_month, today_year = dt.datetime.today(
#         ).isoweekday(), dt.datetime.today(
#         ).month, dt.datetime.today().year
#         for one in all_income:
#             week_days_data[x] = get_amount_for_day(
#                 x, today_day, today_month, today_year)

#     data = {"months": months_data, "days": week_days_data}
#     return JsonResponse({'data': data}, safe=False)



# def last_3months_income_stats(request):
#     todays_date = dt.date.today()
#     three_months_ago = dt.date.today() - dt.timedelta(days=90)
#     income = Expense.objects.filter(owner=request.user,
#                 income_date__gte=three_months_ago, income_date__lte=todays_date)
#     # sources occuring.

#     def get_sources(item):
#         return item.source
#     final = {}
#     sources = list(set(map(get_sources, income)))

#     def get_sources_count(y):
#         new = Expense.objects.filter(source=y)
#         count = new.count()
#         amount = 0
#         for y in new:
#             amount += y.amount
#         return {'count': count, 'amount': amount}

#     for x in income:
#         for y in sources:
#             final[y] = get_sources_count(y)
#     return JsonResponse({'sources_data': final}, safe=False)


# def last_3months_income_source_stats(request):
#     todays_date = dt.date.today()
#     last_month = dt.date.today() - dt.timedelta(days=0)
#     last_2_month = last_month - dt.timedelta(days=30)
#     last_3_month = last_2_month - dt.timedelta(days=30)

#     last_month_income = Expense.objects.filter(owner=request.user,
#                                               income_date__gte=last_month, income_date__lte=todays_date).order_by('income_date')
#     prev_month_income = Expense.objects.filter(owner=request.user,
#                                               income_date__gte=last_month, income_date__lte=last_2_month)
#     prev_prev_month_income = Expense.objects.filter(owner=request.user,
#                                                    income_date__gte=last_2_month, income_date__lte=last_3_month)

#     keyed_data = []
#     this_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
#     prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
#     prev_prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}

#     for x in last_month_income:
#         month = str(x.date)[:7]
#         date_in_month = str(x.date)[:2]
#         if int(date_in_month) <= 7:
#             this_month_data['7th'] += x.amount
#         if int(date_in_month) > 7 and int(date_in_month) <= 15:
#             this_month_data['15th'] += x.amount
#         if int(date_in_month) >= 16 and int(date_in_month) <= 21:
#             this_month_data['22nd'] += x.amount
#         if int(date_in_month) > 22 and int(date_in_month) < 31:
#             this_month_data['29th'] += x.amount

#     keyed_data.append({str(last_month): this_month_data})

#     for x in prev_month_income:
#         date_in_month = str(x.date)[:2]
#         month = str(x.date)[:7]
#         if int(date_in_month) <= 7:
#             prev_month_data['7th'] += x.amount
#         if int(date_in_month) > 7 and int(date_in_month) <= 15:
#             prev_month_data['15th'] += x.amount
#         if int(date_in_month) >= 16 and int(date_in_month) <= 21:
#             prev_month_data['22nd'] += x.amount
#         if int(date_in_month) > 22 and int(date_in_month) < 31:
#             prev_month_data['29th'] += x.amount

#     keyed_data.append({str(last_2_month): prev_month_data})

#     for x in prev_prev_month_income:
#         date_in_month = str(x.date)[:2]
#         month = str(x.date)[:7]
#         if int(date_in_month) <= 7:
#             prev_prev_month_data['7th'] += x.amount
#         if int(date_in_month) > 7 and int(date_in_month) <= 15:
#             prev_prev_month_data['15th'] += x.amount
#         if int(date_in_month) >= 16 and int(date_in_month) <= 21:
#             prev_prev_month_data['22nd'] += x.amount
#         if int(date_in_month) > 22 and int(date_in_month) < 31:
#             prev_prev_month_data['29th'] += x.amount

#     keyed_data.append({str(last_3_month): prev_month_data})
#     return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)



######################################################################## expense search functionality

def expenseSearch(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchStr')
        expenses = Expense.objects.filter(
            Q(expense_by=request.user) &
                (
                    Q(amount__istartswith=search_str) |
                    Q(description__icontains=search_str) |
                    Q(expense_category__title__icontains=search_str) |
                    Q(expense_date__istartswith=search_str) |
                    Q(entry_date__istartswith=search_str)
                )
        ).order_by('-id')

        data = expenses.values('expense_category__title','amount','description','id','expense_date','entry_date')
        for d in data:
            d['category_title'] = d.pop('expense_category__title')
            d['date'] = d.pop('expense_date')
        return JsonResponse(list(data), safe=False)