from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('sign-up/',views.RegistrationView.as_view(), name='signup'),
    path('sign-in/',views.LoginView.as_view(), name='signin'),
    path('sign-out/',views.signOut, name='signout'),
    path(
        'change-password/',auth_views.PasswordChangeView.as_view(
            template_name='dashboard/change-password.html',
            success_url='/'
        ),name='change_password'),


    path('validate-name/',csrf_exempt( views.NameValidationview.as_view()), name='validate-name'),
    path('validate-email/',csrf_exempt( views.EmailValidationview.as_view()), name='validate-email'),
    path('validate-password/',csrf_exempt( views.PasswordValidationview.as_view()), name='validate-password'),
    path('validate-cpassword/',csrf_exempt( views.CPasswordValidationview.as_view()), name='validate-cpassword'),
]