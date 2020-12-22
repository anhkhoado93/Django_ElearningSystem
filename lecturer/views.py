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

def is_lecturer(user):
    return user.user_type == LECTURER

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None)
def homepage(request):
    return render(request, "lecturer/home.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None)
def manageCourse(request):
    lecturerId = request.session['id']
    semester = 201
    if request.method == 'POST':
        re = request.POST.get('myselect')
        semester = re
    result_list = getManagedCourses(lecturerId, semester)
    return render(request, "lecturer/courses.html", { 'courseList': result_list, 'semester': semester })

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None)
def manageCourseDetails(request, semester, courseId):
    lecturerId = request.session['id']
    textbook = getTextbooksOfManagedCourse(lecturerId, semester, courseId) # List(Dict(isbn, name))
    classes = getClassesOfManagedCourse(lecturerId,semester,courseId) #List(classId)
    # allBook = getBookUsedByCourse(courseId)
    return render(request, "lecturer/course_details.html", { 'courseid': courseId, 'textbook': textbook, 'class': classes , 'lockButton': semester != '201'})

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None)
def aboutpage(request):
    return render(request, "lecturer/about.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None) 
def manageClass(request):
    pass

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/login/",redirect_field_name=None)
def classDetails(request):
    pass