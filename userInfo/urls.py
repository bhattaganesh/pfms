from django.urls import path
from . import views
urlpatterns = [
    path('user/profile/', views.userInfo, name='user-info'),
]
