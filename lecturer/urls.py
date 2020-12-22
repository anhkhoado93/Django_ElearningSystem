from django.urls import path
from . import views

app_name = "lecturer"
urlpatterns = [
    path("home", views.homepage, name="home"),
    path("courses", views.manageCourse, name="courses"),
    path("courses/<semester>/<courseId>", views.manageCourseDetails, name="courses"),
    path("about", views.aboutpage, name="about"),
    path("class", views.manageClass, name="class"),
    path("class/<classId>", views.classDetails, name="classDetails")
]