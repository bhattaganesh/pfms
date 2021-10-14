from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='incomes'),
    path('add/', views.addIncome, name='add-income'),
    path('edit/<int:id>/', views.editIncome, name='edit-income'),
    path('details/<int:id>/', views.viewIncome, name='view-income'),
    path('delete/<int:id>/', views.deleteIncome, name='delete-income'),

    path('categories/', views.listAllCategories, name='income-categories'),
    path('add-category/', views.addCategory, name='add-income-category'),
    path('edit-category/<int:id>/', views.editCategory, name='edit-income-category'),
    path('details-category/<int:id>/', views.viewCategory, name='view-income-category'),
    path('delete-category/<int:id>/', views.deleteCategory, name='delete-income-category'),
]
