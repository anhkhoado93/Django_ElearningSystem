from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AssignsTextbook, AttendsClass, Author, Class, Course, Department, Enrolls, Lecturer, ManagesClass, ManagesCourse, Publisher, Publishes, Student, Teaches, Textbook, Uses, Writes)
class DataAdmin(admin.ModelAdmin):
    pass