from django.urls import path
from . import views

app_name = "department"
urlpatterns = [
    path("manage", views.managepage, name="manage"),
    path("manage/<str:courseId>", views.managecoursepage, name="managecourses"),
    path("manage/<str:courseId>/<str:classId>", views.manageclasspage, name="manageclass"),
]