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
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None)
def homepage(request):
    return render(request, "lecturer/home.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None)
def manageCourse(request):
    lecturerId = request.session['id']
    semester = 201
    if request.method == 'POST':
        re = request.POST.get('myselect')
        semester = re
    result_list = getManagedCourses(lecturerId, semester)
    return render(request, "lecturer/courses.html", { 'courseList': result_list, 'semester': semester })

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None)
def manageCourseDetails(request, semester, courseId):
    lecturerId = request.session['id']
    textbook = getTextbooksOfManagedCourse(lecturerId, semester, courseId) # List(Dict(isbn, name))
    for i in textbook: i['Isbn'] = str(i['Isbn'])
    usedBookIsbn = [t['Isbn'] for t in textbook]
    allTextbook = getUsedTextbooksOfManagedCourse(courseId)
    for i in allTextbook: i['Isbn'] = str(i['Isbn'])
    classes = getClassesOfManagedCourse(lecturerId,semester,courseId) #List(classId)
    if request.method == 'POST':
        re = request.POST.get('input')
        try:
            if re not in usedBookIsbn: 
                assignTextbook(lecturerId, semester, courseId, re)
                textbook = getTextbooksOfManagedCourse(lecturerId, semester, courseId) # List(Dict(isbn, name))
                for i in textbook: i['Isbn'] = str(i['Isbn'])
                usedBookIsbn = [t['Isbn'] for t in textbook]
                
            else:
                unassignTextbook(lecturerId, semester, courseId, re)  
                textbook = getTextbooksOfManagedCourse(lecturerId, semester, courseId) # List(Dict(isbn, name))
                for i in textbook: i['Isbn'] = str(i['Isbn'])
                usedBookIsbn = [t['Isbn'] for t in textbook]
        except Exception as e:
            pass
    # allBook = getBookUsedByCourse(courseId)
    return render(request, "lecturer/course_details.html", { 'courseid': courseId, 'usedBookIsbn': usedBookIsbn, 'textbook': textbook, 'allBook': allTextbook, 'class': classes , 'lockButton': semester != '201'})

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None)
def aboutpage(request):
    return render(request, "lecturer/about.html")

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None) 
def manageClass(request):
    lecturerId = request.session['id']
    semester = 201
    if request.method == 'POST':
        re = request.POST.get('myselect')
        semester = re
    classList = getManagedClasses(lecturerId, semester)
    print(classList)
    return render(request, "lecturer/class.html", {'classList': classList, 'semester': semester})

@login_required
@user_passes_test(test_func=is_lecturer,login_url= "/accounts/logout/",redirect_field_name=None)
def classDetails(request, classId):
    lecturerId = request.session['id']
    textbook = getTextbooksOfManagedClass(lecturerId, classId)
    studentList = getStudentsOfManagedClass(lecturerId, classId)
    noStudent = len(studentList)
    return render(request, "lecturer/class_details.html", {'textbook': textbook, 'noStudent': noStudent, 'studentList': studentList})