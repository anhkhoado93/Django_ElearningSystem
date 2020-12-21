from django.urls import path
from . import views

app_name = "student"
urlpatterns = [
    path("home", views.homepage, name="home"),
    path("courses", views.coursepage, name="courses"),
    path("about", views.aboutpage, name="about"),
    path("register", views.register, name="register"),
    path("courses/<str:courseId>", views.course_details, name="courses_details")
]