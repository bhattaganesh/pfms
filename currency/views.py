from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
import os
from django.conf import settings
from .models import Currency
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required(login_url='signin')
def index(request):
    currencies_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        for k, v in data.items():
            currencies_data.append({'name': k, 'value': v})
    # import pdb
    # pdb.set_trace()
    exist = Currency.objects.filter(user=request.user).exists()

    if request.method == 'GET':
        if exist:
            selected_currency = Currency.objects.get(user=request.user).currency.split(" - ")[0]
            return render(request, 'dashboard/currency.html', {'currencies': currencies_data, 'selected_currency_name': selected_currency})
        return render(request, 'dashboard/currency.html', {'currencies': currencies_data})


    if request.method == 'POST':
        if exist:
            curr = Currency.objects.get(user=request.user)
            curr.currency = request.POST['currency']
            curr.save()
            messages.success(request, "Currency is choosed successfully.")
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            curr_name = curr.currency.split(" - ")[0]
            return render(request, 'dashboard/currency.html', {'currencies': currencies_data, 'selected_currency_name': curr_name})
            
        curr = Currency.objects.create(user=request.user, currency=request.POST['currency'])
        curr.save()
        messages.success(request, "Currency is choosed successfully.")
        curr_name = curr.currency.split(" - ")[0]
        return render(request, 'dashboard/currency.html', {'currencies': currencies_data, 'selected_currency_name': curr_name})
