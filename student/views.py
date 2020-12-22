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
    return render(request, "student/home.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def coursepage(request):
    studentId = 1852471
    semester = 191
    result_list = getEnrolledCourses(studentId, semester)
    print(result_list)
    return render(request, "student/courses.html", { 'courseList': result_list })

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def aboutpage(request):
    return render(request, "student/about.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def register(request):
    studentId = 1852471
    if 'semester' not in request.session:
        request.session["semester"] = 201
    totalCredit = getTotalCredits(studentId, request.session["semester"])
    submittedCourse = getEnrolledCourses(studentId=1852471, semester=request.session["semester"])
    openCourseList = getOpenedCourses(request.session["semester"])
    
    if request.method == 'POST':
        re = request.POST.get('input')
        try:
            if re not in submittedCourse:   
                registerCourse(studentId=studentId, courseId=re, semester=request.session["semester"])
            else:
                cancelCourse(studentId=studentId, courseId=re, semester=request.session["semester"])
        except:
            pass
        finally:
            return render(request, "{% url 'student:home' %}")

    return render(request, "student/register.html",  
    {'openCourse': openCourseList, 'submittedCourse': submittedCourse, 'totalCredit': totalCredit  })

@login_required
@user_passes_test(test_func=is_student,login_url= "/accounts/login/",redirect_field_name=None)
def course_details(request, courseId):
    studentId = 1852471
    result_list = getEnrolledCourseInfo(studentId, courseId, request.session['semester'])
    return render(request, 'student/course_details.html', {'info': result_list})