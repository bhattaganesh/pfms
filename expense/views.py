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
from django.views import View
import calendar

# Create your views here.
@login_required(login_url='signin')
def index(request):
    expenses = Expense.objects.filter(expense_by=request.user).order_by('-id')
    if Currency.objects.filter(user=request.user).exists():
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    else:
        messages.info(request, "Please, choose your prefered currency.")
        return redirect('currency')

    return render(request, 'expense/index.html', {
        'currency': currency,
        'expenses': expenses
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
        try:
            def deleteRecord(id):
                expense = Expense.objects.get(id=id)
                expense.delete()

            ids = list(map(deleteRecord, list(ids)))

            return JsonResponse({'status': True, 'msg': 'Deleted Successfully.'})
        except:
            return JsonResponse({'status': False, 'msg': 'Sorry!, error while deleting.'})
    return JsonResponse({'status' : False, 'msg': 'Sorry!, invalid request.'})


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
        try:
            def deleteRecord(id):
                # import pdb; pdb.set_trace()
                category = ExpenseCategory.objects.get(id=id)
                category.delete()

            ids = list(map(deleteRecord, list(ids)))

            return JsonResponse({'status': True, 'msg': 'Deleted Successfully.'})

        except:
            return JsonResponse({'status': False, 'msg': 'Sorry!, error while deleting.'})

    return JsonResponse({'status': False, 'msg': 'Sorry!, invalid request.'})


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


@login_required(login_url='signin')
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


@login_required(login_url='signin')
def monthlyWiseExpense(request):
    all_expenses = Expense.objects.filter(expense_by=request.user)
    if(request.GET['year']):
        year = request.GET['year']
    else:
        year = dt.datetime.today().year
    months_data = {}
    def get_amount_for_month(month, year):
        month_amount = 0
        for one in all_expenses:
            month_, year_ = one.entry_date.month, one.entry_date.year
            if month == month_ and str(year_) == str(year):
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        for one in all_expenses:
            months_data[x] = get_amount_for_month(x,year)
    # import pdb; pdb.set_trace()
    data = {"months": months_data}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='signin')
def weeklyWiseExpense(request):
    all_expenses = Expense.objects.filter(expense_by=request.user)
    if(request.GET['year'] and request.GET['month']):
        year = request.GET['year']
        month = request.GET['month']

    _date = dt.date(int(year), int(month), 1)
    _end_date = _date.replace(day = calendar.monthrange(_date.year, _date.month)[-1])

    weeks_data = {}

    if _end_date.day == 29:
        addDay = 1
    elif _end_date.day == 30:
        addDay = 2
    elif _end_date.day == 31:
        addDay = 3
    else:
        addDay = 0

    firstWeek = _date + dt.timedelta(6)
    secondWeek = firstWeek + dt.timedelta(7)
    thirdWeek = secondWeek + dt.timedelta(7)
    fourthWeek = thirdWeek + dt.timedelta(7+addDay)

    def get_amount_for_week(start_date, end_date):
        week_amount = 0
        expenses_by_week =  all_expenses.filter(entry_date__range=[start_date, end_date])
        for expense in expenses_by_week:
            week_amount += expense.amount
        return week_amount

    weeks_data[f"{_date.day} - {firstWeek.day}"] = get_amount_for_week(_date, firstWeek)
    weeks_data[f"{firstWeek.day} - {secondWeek.day}"] = get_amount_for_week(firstWeek ,secondWeek)
    weeks_data[f"{secondWeek.day} - {thirdWeek.day}"] = get_amount_for_week(secondWeek ,thirdWeek)
    weeks_data[f"{thirdWeek.day} - {fourthWeek.day}"] = get_amount_for_week(thirdWeek, fourthWeek)

    
    data = {"weeks": weeks_data, 'month': _date.strftime('%B')}
    # import pdb; pdb.set_trace()

    return JsonResponse({'data': data}, safe=False)



######################################################################## only for learning purpose (test)
class indexTest(View):
    def get(self, request):
        expenses = Expense.objects.filter(expense_by=request.user).order_by('-id')
        if Currency.objects.filter(user=request.user).exists():
            currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
        else:
            messages.info(request, "Please, choose your prefered currency.")
            return redirect('currency')

        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # first_page = paginator.page(1).object_list
        # page_range = paginator.page_range

        # import pdb; pdb.set_trace()

        return render(request, 'expense/index-test.html', {
            'currency': currency,
            'page_obj': page_obj
    })


@login_required(login_url='signin')
def deleteExpensesTest(request):
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