from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.

def homepage(request):
    return render(request, "student/home.html")

def coursepage(request):
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

def register(request):
     if request.method == 'POST':
        courseId = int(request.POST.get('courseId'))
        with connection.cursor() as cursor:
            cursor.callproc('studentEnrollCourse', [studentId, semester, courseId])
            result = cursor.fetchall()
            result_list = [{'courseId': i[0], 'courseName': i[1]} for i in result]
    return render(request, "student/register.html")

def course_details(request, courseId):
    studentId = None
    semester = None
    result_list = None

    with connection.cursor() as cursor:
        cursor.callproc('studentGetClassesAndLecturers', [studentId, semester])
        result = cursor.fetchall()
        for i in result:
            if i[0] == courseId:
                result_list = {'courseName': i[1], 'courseId': i[0], 'classId': i[2], 'lecturerName': i[3]}
                break
    result_list['bookTitle'] = []
    with connection.cursor() as cursor:
        cursor.callproc('studentGetTextbooksOfEnrolledCourses', [studentId, semester])
        result = cursor.fetchall()
        for i in result:
            if i[0] == courseId:
                result_list['bookTitle'] += [i[2]]

    return render(request, 'student/course_details.html', {'info': result_list})