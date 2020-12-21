from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from .api import *
# Create your views here.

def homepage(request):
    return render(request, "student/home.html")

def coursepage(request):
    studentId = 1852471
    semester = 191
    result_list = getEnrolledCourses(studentId, semester)
    print(result_list)
    return render(request, "student/courses.html", { 'courseList': result_list })

def aboutpage(request):
    return render(request, "student/about.html")

def register(request):
    # get available course getOpenedCourses
    semester = 201
    lst = getOpenedCourses(semester)
    if 'regCourse' not in request.session:
        request.session["regCourse"] = []
    if request.method == 'POST':
        print(request.session["regCourse"])
        re = request.POST.get('input')
        re = re.split(' ')
        if re[0] == 'select':
            request.session["regCourse"] += [re[1]]
            print(request.session["regCourse"])
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"],
        'openCourse': lst})
        elif re[0] == 'remove':
            request.session["regCourse"] = list(filter(lambda x: x != re[1], request.session["regCourse"]))
            print(request.session["regCourse"])
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"],
        'openCourse': lst})
    return render(request, "student/register.html", {
        'regCourse': request.session["regCourse"],
        'openCourse': lst
        })

def course_details(request, courseId):
    studentId = 1852471
    semester = 201
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