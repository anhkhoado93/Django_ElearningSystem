from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm

# Create your views here.

def signup_user(request):
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         userid = form.cleaned_data['userid']
    #         username = form.cleaned_data['username']
    #         user_type = form.cleaned_data['usertype']
    #         name = form.cleaned_data['name']
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #         db = 'default'
    #         try:
    #             if user_type == OFFICE:
    #                 db = 'office'
    #             elif user_type == DEPARTMENT:
    #                 db = 'department'
    #             elif user_type == LECTURER:
    #                 db = 'lecturer'
    #                 lecturer = Lecturer(userid, name)
    #                 lecturer.save()
    #             elif user_type == STUDENT:
    #                 db = 'student'
    #                 student = Student(userid, name, 'active')
    #                 student.save()
    #             user = User.objects.using(db).create_user(
    #                 user_id=userid,
    #                 username=username,
    #                 email=email,
    #                 password=password,
    #                 user_type=user_type
    #             )
    #             user.save()
    #         except:
    #             return HttpResponse("User already exists.")
    # else:
    #     form = UserRegistrationForm()

    return HttpResponse("Hello, World!")