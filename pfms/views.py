from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
@login_required(login_url='signin')
def index(request):
    # if request.method == 'POST':
    #     password_form = PasswordChangeForm(instance = request.user, data = request.POST)
    #     if password_form.is_valid():
    #         password_form.save()
    #         update_session_auth_hash(request, password_form.user)  # <-- keep the user loged after password change
    #         messages.success(request, 'Your password was successfully updated!', extra_tags='safe')
    #     else:
    #         messages.error(request, 'Something went wrong', extra_tags='safe')
    # else:
    #     password_form = PasswordChangeForm(instance = request.user)
    # return render(request, 'registration/password_change_form.html', {'password_form': password_form})
    return render(request, 'dashboard/dashboard.html')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)