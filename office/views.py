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
@user_passes_test(test_func=is_office,login_url= "/accounts/logout/",redirect_field_name=None)
def homepage(request):
    request.session['semester'] = 201
    return render(request, "office/home.html")

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/logout/",redirect_field_name=None)
def deppage(request):
    dep = getDepartments()
    return render(request, "office/deps.html", {'departments': dep})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/logout/",redirect_field_name=None)
def coursepage(request, depsId):
    courses = getCoursesOfDepartment(depsId)
    return render(request, "office/courses.html", {'departments': depsId, 'courses': courses})

def classpage(request, depsId, courseId):
    classes = getClassesOfCourse(request.session['semester'], courseId)
    print(classes)
    return render(request, "office/class.html", {'departments': depsId, 'courseId': courseId, 'classes': classes})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/logout/",redirect_field_name=None)
def classinfopage(request, depsId, courseId, classId):
    studentList = getStudentsOfClass(classId)
    print(studentList)
    lecturerList = getLecturersOfClass(classId)
    return render(request, "office/class_details.html", {'student':studentList, 'lecturer': lecturerList})

@login_required
@user_passes_test(test_func=is_office,login_url= "/accounts/logout/",redirect_field_name=None)
def enroll(request):
    if request.method == 'POST':
        re = request.POST.get('value')
        re = re.split(' ')
        assignEnrollment(re[0], re[1])
    lst = list(map(lambda x: {
        'StudentId': x['StudentId'],
        'CourseId': x['CourseId'] ,
        'availableC': getClassesOfCourse(request.session['semester'], x['CourseId'])} ,getUnassignedEnrollment(request.session['semester'])))

    return render(request, "office/enroll.html", {'list': lst })