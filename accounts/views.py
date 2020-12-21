from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['id'] = user.user_id
            request.session['user_type'] = user.user_type
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username or Password is incorrect!!",
                extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, "accounts/login.html")

def logout_user(request):
    logout(request)
    return redirect('home')
