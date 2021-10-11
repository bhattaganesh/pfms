from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'expense/index.html')

def addExpense(request):
    return render(request, 'expense/add-expense.html')