from django.urls import path
from . import views

app_name = "administrator"
urlpatterns = [
    # TODO: Add urls here
    path("", views.signup_user, name="createUser")
]