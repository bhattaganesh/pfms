from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index, name='expenses'),
    path('add/', views.addExpense, name='add-expense'),
    path('edit/<int:id>/', views.editExpense, name='edit-expense'),
    path('details/<int:id>/', views.viewExpense, name='view-expense'),
    path('delete/<int:id>/', views.deleteExpense, name='delete-expense'),
    path('delete/', views.deleteExpenses, name='delete-expenses'),

# ############################################################ Expense Category

    path('categories/', views.listAllCategories, name='expense-categories'),
    path('add-category/', views.addCategory, name='add-category'),
    path('edit-category/<int:id>/', views.editCategory, name='edit-category'),
    path('details-category/<int:id>/', views.viewCategory, name='view-category'),
    path('delete-category/<int:id>/', views.deleteCategory, name='delete-category'),
    path('delete-category/', views.deleteCategories, name='delete-categories'),

# ############################################################ Expense summary
    path('summary/', views.expenseSummary, name='expense-summary'),
    path('expense-summary-by-category/', views.expenseSummaryByCategory, name='expense-summary-by-category'),
    path('monthly/', views.monthlyWiseExpense, name='monthly-expense'),
    path('weekly/', views.weeklyWiseExpense, name='weekly-expense'),

# ############################################################ for learning purpose
    path('test/', views.indexTest.as_view(), name='expenses-test'),
    path('search/test/', csrf_exempt(views.expenseSearch), name='expense-search'),
    path('delete/test/', views.deleteExpensesTest, name='delete-expenses-test'),


]
