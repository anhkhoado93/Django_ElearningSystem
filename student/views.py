from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from .api import *
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def is_student(user):
    return user.user_type == user.USER_TYPE_CHOICES[3]

# @cache_control(no_cache=True, must_revalidate=True, no_store=True) # to prevent user back button after logging out
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
    studentId = 1852471
    if 'semester' not in request.session:
        request.session["semester"] = 201
    submittedCourse = getEnrolledCourses(studentId=1852471, semester=request.session["semester"])
    if 'regCourse' not in request.session:
        request.session["regCourse"] = []
        if submittedCourse:
            request.session["regCourse"] += [r['CourseId'] for r in submittedCourse]
    openCourseList = getOpenedCourses(request.session["semester"])
    if request.method == 'POST':
        re = request.POST.get('input')
        re = re.split(' ')
        if re[0] == 'select':
            request.session["regCourse"] += [re[1]]
        elif re[0] == 'remove':
            request.session["regCourse"] = list(filter(lambda x: x != re[1], request.session["regCourse"]))
        elif re[0] == 'semester':
            request.session['semester'] = re[1]
        elif re[0] == 'submit':
            for r in request.session["regCourse"]:
                registerCourse(studentId=studentId, courseId=r, semester=request.session["semester"])
            return render(request, "{% url 'student:home' %}")

    return render(request, "student/register.html", {'regCourse': request.session["regCourse"],'openCourse': openCourseList, 'submittedCourse': submittedCourse })

@login_required
@user_passes_test(test_func=is_student,login_url= "{url accounts:login}",redirect_field_name=None)
def course_details(request, courseId):
    studentId = 1852471
    result_list = getEnrolledCourseInfo(studentId, courseId, request.session['semester'])
    return render(request, 'student/course_details.html', {'info': result_list})