from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

# ############################################################ Income 

    path('', views.index, name='incomes'),
    path('add/', views.addIncome, name='add-income'),
    path('edit/<int:id>/', views.editIncome, name='edit-income'),
    path('details/<int:id>/', views.viewIncome, name='view-income'),
    path('delete/<int:id>/', views.deleteIncome, name='delete-income'),
    path('delete/', views.deleteIncomes, name='delete-incomes'),

# ############################################################ Income category

    path('categories/', views.listAllCategories, name='income-categories'),
    path('add-category/', views.addCategory, name='add-income-category'),
    path('edit-category/<int:id>/', views.editCategory, name='edit-income-category'),
    path('details-category/<int:id>/', views.viewCategory, name='view-income-category'),
    path('delete-category/<int:id>/', views.deleteCategory, name='delete-income-category'),
    path('delete-category/', views.deleteCategories, name='delete-income-categories'),


# ############################################################ Income summary
    path('summary/', views.incomeSummary, name='income-summary'),
    path('income-summary-by-category/', views.incomeSummaryByCategory, name='income-summary-by-category'),
    path('monthly/', views.monthlyWiseIncome, name='monthly-income'),
    path('weekly/', views.weeklyWiseIncome, name='weekly-income'),
]

