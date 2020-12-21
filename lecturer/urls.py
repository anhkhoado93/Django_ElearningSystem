from django.urls import path
from . import views

app_name = "student"
urlpatterns = [
    path("home", views.homepage, name="home"),
    path("courses", views.manageCourse, name="courses"),
    path("about", views.aboutpage, name="about"),
    path("class", views.manageClass, name="register"),
    path("class/<int:classId>", views.classDetails, name="classDetails")
]