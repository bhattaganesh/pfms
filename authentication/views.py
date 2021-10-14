from os import name
from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
# from django.contrib.auth.models import User
from authentication.models import User
from django.contrib import messages
from  validate_email import validate_email
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        context = {'fieldValues': request.POST}

        if len(name) <= 0:
            messages.error(request,'Name should not be empty.')
            return render(request, 'auth/register.html', context)

        if len(email) <= 0:
            messages.error(request,'Email should not be empty.')
            return render(request, 'auth/register.html', context)

        if not validate_email(email):
            messages.error(request,'Email should be valid email.')
            return render(request, 'auth/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request,'Sorry, this email has been already taken.')
            return render(request, 'auth/register.html', context)

        if len(password) <= 0:
            messages.error(request,'Password should not be empty.')
            return render(request, 'auth/register.html', context)

        if len(password) < 8:
            messages.error(request,'Password should have atleast length 8.')
            return render(request, 'auth/register.html', context)

        if password != cpassword:
            messages.error(request,'Confirmation password does not match with password.')
            return render(request, 'auth/register.html', context)

        user = User.objects.create_user(name=name, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully.')
        return render(request, 'auth/login.html')

class NameValidationview(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['name']


        if len(name) == 0:
            return JsonResponse({
                'name_error': 'Name should not be empty.'
            }, status= 400)
        if len(name) < 3 or len(name) > 30:
            return JsonResponse({
                'name_error': 'Name should have aleast 3 and atmost 30 characters.'
            }, status= 400)
        if str(name).isnumeric():
            return JsonResponse({
                'name_error': 'Name should not numeric.'
            }, status= 400),
        return JsonResponse({'name_valid': True})


class EmailValidationview(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid' }, status= 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email has been already taken.' }, status= 400)
        return JsonResponse({'email_valid': True})


class PasswordValidationview(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        if len(password) == 0:
            return JsonResponse({'password_error': 'Password should not be empty.'}, status= 400)
        if len(password) < 8:
            return JsonResponse({'password_error': 'Password should have atleast length 8.'}, status= 400)
        return JsonResponse({'password_valid': True})
        

class CPasswordValidationview(View):
    def post(self, request):
        data = json.loads(request.body)
        cpassword = data['cpassword']
        password = data['password']

        if len(cpassword) == 0:
            return JsonResponse({'cpassword_error': 'Confirmation  password should not be empty.'}, status= 400)

        # if len(cpassword) < 8:
        #     return JsonResponse({'cpassword_error': 'Confirmation  password should have atleast length 8.'}, status= 400)

        if password != cpassword:
            return JsonResponse({'cpassword_error': 'Confirmation password does not match with password.' }, status= 400)
        return JsonResponse({'cpassword_valid': True})
        


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        context = {'fieldValues': request.POST}

        if len(email) <= 0:
            messages.error(request,'Email should not be empty.')
            return render(request, 'auth/login.html', context)

        if not validate_email(email):
            messages.error(request,'Email should be valid email.')
            return render(request, 'auth/login.html', context)

        if len(password) <= 0:
            messages.error(request,'Password should not be empty.')
            return render(request, 'auth/login.html', context)

        if len(password) < 8:
            messages.error(request,'Password should have atleast length 8.')
            return render(request, 'auth/login.html', context)

        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, f'Welcome {user.name}, you are now logged in.')
            return redirect('dashboard')

        messages.error(request, f'invalid login credentials, try again.')
        return render(request, 'auth/login.html', context)

def signOut(request):
    messages.success(request, 'You have been logged out.')
    auth.logout(request)
    return redirect('signin')
