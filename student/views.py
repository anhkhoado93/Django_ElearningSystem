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

def is_student(user):
    return user.user_type == STUDENT
    
# @cache_control(no_cache=True, must_revalidate=True, no_store=True) # to prevent user back button after logging out
@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def homepage(request):
    request.session["semester"] = 201
    return render(request, "student/home.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def coursepage(request):
    studentId = request.session['id']
    semester = 201
    if request.method == 'POST':
        re = request.POST.get('myselect')
        semester = re
    result_list = getEnrolledCourses(studentId, semester)
    return render(request, "student/courses.html", { 'courseList': result_list, 'semester': semester })

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def aboutpage(request):
    return render(request, "student/about.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def register(request):
    studentId = request.session['id']
    request.session["semester"] = 201
    submittedCourse = [i['CourseId']  for i in getEnrolledCourses(studentId=request.session['id'], semester=request.session["semester"])]
    openCourseList = getOpenedCourses(request.session["semester"])
    if request.method == 'POST':
        re = request.POST.get('input')
        try:
            if re not in submittedCourse:   
                registerCourse(studentId=studentId, courseId=re, semester=request.session["semester"])
                submittedCourse += [re]
            else:
                cancelCourse(studentId=studentId, courseId=re, semester=request.session["semester"])
                submittedCourse = list(filter(lambda x: x != re ,submittedCourse))
        except:
            pass
    totalCredit = getTotalCredits(studentId, request.session["semester"])
    return render(request, "student/register.html",  
    {'openCourse': openCourseList, 'submittedCourse': submittedCourse, 'totalCredit': totalCredit  })

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def course_details(request, courseId):
    studentId = request.session['id']
    result_list = getEnrolledCourseInfo(studentId, courseId, request.session['semester'])   
    return render(request, 'student/course_details.html', {'info': result_list})