from django.urls import path
from . import views

app_name = "department"
urlpatterns = [
    path("manage", views.managepage, name="manage"),
    path("manage/<str:courseId>", views.managecoursepage, name="managecourses"),
    path("manage/<str:courseId>/<str:classId>", views.manageclasspage, name="manageclass"),
    # path("view", views.viewpage, name="courses"),
    # path("view/<str:courseId>", views.coursepage, name="courses"),
    # path("view/<str:courseId>/<str:classId>", views.classpage, name="class")
]