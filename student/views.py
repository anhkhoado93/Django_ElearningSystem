from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def homepage(request):
    return render(request, "student/home.html")

def coursepage(request):
    

    return render(request, "student/course.html")

def aboutpage(request):
    return render(request, "student/about.html")