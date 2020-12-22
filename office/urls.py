from django.urls import path
from . import views

app_name = "office"
urlpatterns = [
    path("home", views.homepage, name="home"),
    path("deps", views.deppage, name="department"),
    path("deps/<depsId>", views.viewpage, name="view"),
    path("deps/<deps>/<courseId>", views.coursepage, name="courses"),
    path("deps/<deps>/<courseId>/<classId>", views.classpage, name="class")
]