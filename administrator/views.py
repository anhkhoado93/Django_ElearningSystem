from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from .api import *
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

OFFICE = 1
DEPARTMENT = 2
LECTURER = 3
STUDENT = 4
ADMIN = 5
def is_admin(user):
    return user.user_type == ADMIN
    
# # @cache_control(no_cache=True, must_revalidate=True, no_store=True) # to prevent user back button after logging out
# @login_required
# @user_passes_test(test_func=is_admin,login_url= "/accounts/logout/",redirect_field_name=None)
def signup_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            userid = form.cleaned_data['userid']
            usertype = form.cleaned_data['usertype']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            create_user(userid, usertype, username, email, password, name)
            # return redirect("/home")
    return render(request, "administrator/add_user.html", {"form": UserRegistrationForm()})