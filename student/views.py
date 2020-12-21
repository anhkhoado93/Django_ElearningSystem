from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
# Create your views here.

def homepage(request):
    return render(request, "student/home.html")

def coursepage(request):
    studentId = 1852471
    semester = 191 
    result_list = None
    with connection.cursor() as cursor:
        cursor.execute(' \
        SELECT E.CourseId, C.CourseName\
        FROM ENROLLS AS E JOIN COURSE AS C ON E.CourseId = C.CourseId AND E.StudentId = {} AND E.Semester = {}\
        '.format(studentId, semester))
        result = cursor.fetchall()
        result_list = [{'courseId': i[0], 'courseName': i[1]} for i in result]
    return render(request, "student/courses.html", { 'courseList': result_list })

def aboutpage(request):
    return render(request, "student/about.html")

def register(request):
    if 'regCourse' not in request.session:
        request.session["regCourse"] = []
    if request.method == 'POST':
        print(request.session["regCourse"])
        re = request.POST.get('input')
        re = re.split(' ')
        if re[0] == 'select':
            request.session["regCourse"] += [re[1]]
            print(request.session["regCourse"])
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"]})
        elif re[0] == 'remove':
            request.session["regCourse"] = list(filter(lambda x: x != re[1], request.session["regCourse"]))
            print(request.session["regCourse"])
            return render(request, "student/register.html", {'regCourse': request.session["regCourse"]})
    return render(request, "student/register.html", {'regCourse': request.session["regCourse"]})

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