from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('sign-up/',views.RegistrationView.as_view(), name='signup'),
    path('sign-in/',views.LoginView.as_view(), name='signin'),
    path('sign-out/',views.signOut, name='signout'),
    path(
        'change-password/',auth_views.PasswordChangeView.as_view(
            template_name = 'dashboard/change-password.html',
            # success_message = 'Password changed successfully, Please login again!',
            success_url = '/sign-out'
        ),name='change_password'),

    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='auth/password-reset.html',
        email_template_name = 'auth/password-reset-email.html',
        ),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='auth/password-reset-confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(template_name='auth/password-reset-done.html'),
        name='password_reset_done'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='auth/password-reset-complete.html'),
        name='password_reset_complete'),

    path('user/delete-account/', views.deleteAccount, name='delete-account'),

    path('validate-name/',csrf_exempt( views.NameValidationview.as_view()), name='validate-name'),
    path('validate-email/',csrf_exempt( views.EmailValidationview.as_view()), name='validate-email'),
    path('validate-password/',csrf_exempt( views.PasswordValidationview.as_view()), name='validate-password'),
    path('validate-cpassword/',csrf_exempt( views.CPasswordValidationview.as_view()), name='validate-cpassword'),
]