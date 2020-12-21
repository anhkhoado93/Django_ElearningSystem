from accounts.models import User
from .models import Lecturer, Student

OFFICE = 1
DEPARTMENT = 2
LECTURER = 3
STUDENT = 4

def create_user(id, user_type, username, email, password, name=None):
    db = 'default'
    try:
        if user_type == OFFICE:
            db = 'office'
        elif user_type == DEPARTMENT:
            db = 'department'
        elif user_type == LECTURER:
            db = 'lecturer'
            lecturer = Lecturer(id, name)
            lecturer.save()
        elif user_type == STUDENT:
            db = 'student'
            student = Student(id, name, 'active')
            student.save()
        user = User.objects.using(db).create_user(
            user_id=id,
            username=username,
            email=email,
            password=password,
            user_type=user_type
        )
        user.save()
    except:
        raise Exception("User already exists.")