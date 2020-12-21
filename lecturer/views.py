from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.

def is_lecturer(user):
    pass

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "{url accounts:login}",redirect_field_name=None)
def homepage(request):
    return render(request, "student/home.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "{url accounts:login}",redirect_field_name=None)
def manageCourse(request):
    studentId = None
    semester = None
    result_list = None
    with connection.cursor() as cursor:
        cursor.callproc('studentGetClassesAndLecturers', [studentId, semester])
        result = cursor.fetchall()
        result_list = [{'courseId': i[0], 'courseName': i[1]} for i in result]
    return render(request, "student/course.html", { 'courseList': result_list })

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "{url accounts:login}",redirect_field_name=None)
def aboutpage(request):
    return render(request, "student/about.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "{url accounts:login}",redirect_field_name=None) 
def manageClass(request):
    pass

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "{url accounts:login}",redirect_field_name=None)
def classDetails(request):
    pass