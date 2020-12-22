from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from .api import *
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

OFFICE = 1
DEPARTMENT = 2
LECTURER = 3
STUDENT = 4

def is_office(user):
    return user.user_type == OFFICE
    
# @cache_control(no_cache=True, must_revalidate=True, no_store=True) # to prevent user back button after logging out
@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/login/",redirect_field_name=None)
def homepage(request):
    return render(request, "office/home.html")

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/login/",redirect_field_name=None)
def deppage(request):
    dep = getDepartments()
    return render(request, "office/deps.html", {'departments': dep})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/login/",redirect_field_name=None)
def viewpage(request, dep):
    courses = getCoursesOfDepartment(dep)
    return render(request, "office/view.html", {'departments': dep, 'courses': courses})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/login/",redirect_field_name=None)
def coursepage(request, courseId):
    semester = 201
    classList = getClassesOfCourse(semester, courseId)
    return render(request, "office/course.html", {'departments': dep, 'courses': courses, 'classList': classList})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/login/",redirect_field_name=None)
def classpage(request, courseId, classId):
    return render(request, "office/class.html", {'courseId': courseId, 'classId': classId})