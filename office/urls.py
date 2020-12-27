from django.urls import path
from . import views

app_name = "office"
urlpatterns = [
    path("home", views.homepage, name="home"),
    path("deps", views.deppage, name="department"),
    path("deps/<int:depsId>", views.coursepage, name="courses"),
    path("deps/<str:depsId>/<str:courseId>", views.classpage, name="class"),
    path("deps/<str:depsId>/<str:courseId>/<str:classId>", views.classinfopage, name="classinfopage"),
    path("enroll",views.enroll, name="enroll")
]