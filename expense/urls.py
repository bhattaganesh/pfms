from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='expenses'),
    path('add/', views.addExpense, name='add-expense'),
    path('edit/<int:id>/', views.editExpense, name='edit-expense'),
]
