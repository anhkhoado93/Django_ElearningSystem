from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib.auth.decorators import user_passes_test
from .api import *
# Create your views here.

OFFICE = 1
DEPARTMENT = 2
LECTURER = 3
STUDENT = 4

def is_department(user):
    return user.user_type == DEPARTMENT

@login_required
@user_passes_test(test_func=is_department,login_url= "/accounts/logout/",redirect_field_name=None)
def managepage(request):
    depId = request.session['id']
    if 'semester' not in request.session:
        request.session['semester'] = 201
    allCourses = getCourses(depId, request.session['semester'])
    return render(request, "department/managepage.html", {"allCourses": allCourses})

@login_required
@user_passes_test(test_func=is_department,login_url= "/accounts/logout/",redirect_field_name=None)
def managecoursepage(request, courseId):
    depId = request.session['id']
    if 'semester' not in request.session:
        request.session['semester'] = 201
    if request.method == "POST":
        re = request.POST.get("value")
        re = re.split(' ')
        if re[0] == 'add':
            openClass(depId, request.session['semester'], courseId)
        elif re[0] == 'remove':
            closeClass(depId, request.session['semester'], courseId, re[1])
    classes = getClassesOfCourse(depId, request.session['semester'], courseId)
    return render(request, "department/managecoursepage.html", {"courseId": courseId,"classes": classes})

@login_required
@user_passes_test(test_func=is_department,login_url= "/accounts/logout/",redirect_field_name=None)
def manageclasspage(request, courseId, classId):
    depId = request.session['id']
    if 'semester' not in request.session:
        request.session['semester'] = 201
    if request.method == "POST":
        re = request.POST.get("value")
        assignLecturerToClass(depId,classId,re)
    lecturerByWeek = getLecturersPerWeek(depId, request.session['semester'], classId)
    allLecturer = getWorkingLecturers(depId, request.session['semester'])
    return render(request, "department/manageclasspage.html", {"lecturerByWeek": lecturerByWeek, 'allLecturer': allLecturer})