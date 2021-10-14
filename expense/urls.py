from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='expenses'),
    path('add/', views.addExpense, name='add-expense'),
    path('edit/<int:id>/', views.editExpense, name='edit-expense'),
    path('details/<int:id>/', views.viewExpense, name='view-expense'),
    path('delete/<int:id>/', views.deleteExpense, name='delete-expense'),

    path('categories/', views.listAllCategories, name='expense-categories'),
    path('add-category/', views.addCategory, name='add-category'),
    path('edit-category/<int:id>/', views.editCategory, name='edit-category'),
    path('details-category/<int:id>/', views.viewCategory, name='view-category'),
    path('delete-category/<int:id>/', views.deleteCategory, name='delete-category'),
]
