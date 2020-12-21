from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from .api import *
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def is_student(user):
    return user.user_type == user.USER_TYPE_CHOICES[3]

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
def homepage(request):
    return render(request, "student/home.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
def coursepage(request):
    studentId = 1852471
    semester = 191
    result_list = getEnrolledCourses(studentId, semester)
    print(result_list)
    return render(request, "student/courses.html", { 'courseList': result_list })

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
def aboutpage(request):
    return render(request, "student/about.html")

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
def register(request):
    if 'semester' not in request.session:
        request.session["semester"] = 201
    if 'regCourse' not in request.session:
        request.session["regCourse"] = []
    lst = getOpenedCourses(request.session["semester"])
    if request.method == 'POST':
        re = request.POST.get('input')
        re = re.split(' ')
        if re[0] == 'select':
            request.session["regCourse"] += [re[1]]
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"], 'openCourse': lst})
        elif re[0] == 'remove':
            request.session["regCourse"] = list(filter(lambda x: x != re[1], request.session["regCourse"]))
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"], 'openCourse': lst})
        elif re[0] == 'semester':
            request.session['semester'] = re[1]
    return render(request, "student/register.html", {'regCourse': request.session["regCourse"],'openCourse': lst })

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
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