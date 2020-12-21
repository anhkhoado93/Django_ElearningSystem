from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.

def homepage(request):
    return render(request, "student/home.html")

def manageCourse(request):
    studentId = None
    semester = None
    result_list = None
    with connection.cursor() as cursor:
        cursor.callproc('studentGetClassesAndLecturers', [studentId, semester])
        result = cursor.fetchall()
        result_list = [{'courseId': i[0], 'courseName': i[1]} for i in result]
    return render(request, "student/course.html", { 'courseList': result_list })

def aboutpage(request):
    return render(request, "student/about.html")
    
def manageClass(request):
    pass

def classDetails(request):
    pass