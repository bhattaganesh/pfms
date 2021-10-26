from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.forms import AddIncomeForm, AddCateoryForm
from django.contrib import messages
from django.db.models import Q
from income.models import Income, IncomeCategory
from django.core.paginator import Paginator
from currency.models import Currency
import datetime as dt
import calendar
# Create your views here.
@login_required(login_url='signin')
def index(request):
    incomes = Income.objects.filter(income_by=request.user)[::-1]
    if Currency.objects.filter(user=request.user).exists():
        currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
    else:
        messages.info(request, "Please, choose your prefered currency.")
        return redirect('currency')

    return render(request, 'income/index.html', {
        'currency': currency,
        'incomes': incomes
        })


@login_required(login_url='signin')
def addIncome(request):
    if not Currency.objects.filter(user=request.user).exists():
        messages.warning(request, "Please, choose your prefered currency.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
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
    if request.method =="POST":
        try:
            income = Income.objects.get(id=id)
            income.delete()
            messages.success(request, "Income Deleted successfully.")
        except:
            messages.error(request, "Sorry, error while deleting income.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='signin')
def deleteIncomes(request):
    if request.method =="POST":
        ids = list(map(lambda id:int(id), request.POST['ids'].split(",")))
        try:
            def deleteRecord(id):
                income = Income.objects.get(id=id)
                income.delete()

            ids = list(map(deleteRecord, list(ids)))

            return JsonResponse({'status': True, 'msg': 'Deleted Successfully.'})
        except:
            return JsonResponse({'status': False, 'msg': 'Sorry!, error while deleting.'})
    return JsonResponse({'status' : False, 'msg': 'Sorry!, invalid request.'})

###################################################################################  for income category


@login_required(login_url='signin')
def listAllCategories(request):
    categories = IncomeCategory.objects.filter(Q(created_by=request.user) | Q(created_by__is_admin=True))[::-1]
    return render(request, 'income-category/index.html', {'categories': categories,}) 

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
    if request.method =="POST":
        try:
            category = IncomeCategory.objects.get(id=id)
            category.delete()
            messages.success(request, "Income Category Deleted successfully.")
        except:
            messages.error(request, "Sorry, error while deleting income category.")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request, "Sorry, invalid request.")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='signin')
def deleteCategories(request):
    if request.method =="POST":
        ids = list(map(lambda id:int(id), request.POST['ids'].split(",")))
        try:
            def deleteRecord(id):
                # import pdb; pdb.set_trace()
                category = IncomeCategory.objects.get(id=id)
                category.delete()

            ids = list(map(deleteRecord, list(ids)))

            return JsonResponse({'status': True, 'msg': 'Deleted Successfully.'})

        except:
            return JsonResponse({'status': False, 'msg': 'Sorry!, error while deleting.'})

    return JsonResponse({'status' : False, 'msg': 'Sorry!, invalid request.'})

###################################################################################  for income summary

@login_required(login_url='signin')
def incomeSummaryByCategory(request):
    todays_date = dt.date.today()
    day = int(request.GET['day'])
    # import pdb; pdb.set_trace()
    six_month_ago = todays_date - dt.timedelta(days=day)
    incomes = Income.objects.filter(income_by=request.user, entry_date__gte=six_month_ago, entry_date__lte=todays_date)
    finalrep = {}


    def get_category(income):
        return income.income_category
    
    category_list = list(set(map(get_category, incomes)))

    def get_income_category_amount(category):
        amount = 0
        filter_by_category = incomes.filter(income_category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount

    for x in incomes:
        for y in category_list:
            finalrep[y.title] = get_income_category_amount(y)
    # import pdb; pdb.set_trace()
    return JsonResponse({'category_data': finalrep}, safe=False)

@login_required(login_url='signin')
def incomeSummary(request):
    if not Currency.objects.filter(user=request.user).exists():
        messages.info(request, "Please, choose your prefered currency.")
        return redirect('currency')

    incomes = Income.objects.filter(income_by=request.user)
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
    for income in incomes:
        if income.entry_date == today:
            todays_amount += income.amount
            todays_count += 1
            
        if income.entry_date >= week_ago:
            this_weeks_amount += income.amount
            this_weeks_count += 1

        if income.entry_date >= month_ago:
            this_months_amount += income.amount
            this_months_count += 1

        if income.entry_date >= year_ago:
            this_years_amount += income.amount
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
    return render(request, 'income/income-summary.html', context)

@login_required(login_url='signin')
def monthlyWiseIncome(request):
    all_incomes = Income.objects.filter(income_by=request.user)
    if(request.GET['year']):
        year = request.GET['year']
    else:
        year = dt.datetime.today().year
    months_data = {}
    def get_amount_for_month(month, year):
        month_amount = 0
        for one in all_incomes:
            month_, year_ = one.entry_date.month, one.entry_date.year
            if month == month_ and str(year_) == str(year):
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        for one in all_incomes:
            months_data[x] = get_amount_for_month(x,year)
    # import pdb; pdb.set_trace()
    data = {"months": months_data}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='signin')
def weeklyWiseIncome(request):
    all_incomes = Income.objects.filter(income_by=request.user)
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
        incomes_by_week =  all_incomes.filter(entry_date__range=[start_date, end_date])
        for income in incomes_by_week:
            week_amount += income.amount
        return week_amount

    weeks_data[f"{_date.day} - {firstWeek.day}"] = get_amount_for_week(_date, firstWeek)
    weeks_data[f"{firstWeek.day} - {secondWeek.day}"] = get_amount_for_week(firstWeek ,secondWeek)
    weeks_data[f"{secondWeek.day} - {thirdWeek.day}"] = get_amount_for_week(secondWeek ,thirdWeek)
    weeks_data[f"{thirdWeek.day} - {fourthWeek.day}"] = get_amount_for_week(thirdWeek, fourthWeek)

    
    data = {"weeks": weeks_data, 'month': _date.strftime('%B')}
    # import pdb; pdb.set_trace()

    return JsonResponse({'data': data}, safe=False)
