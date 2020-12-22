from django.db import connection


def getManagedCourses(lecturerId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetManagedCourses', [lecturerId, semester])
        result = [{'CourseId': res[0], 'CourseName': res[1]} for res in cursor.fetchall()]
    return result

def getUsedTextbooksOfManagedCourse(courseId):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetUsedTextbooksOfManagedCourse', [courseId])
        result = [{'Isbn': res[0], 'Title': res[1]} for res in cursor.fetchall()]
    return result

def getTextbooksOfManagedCourse(lecturerId, semester, courseId):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetTextbooksOfManagedCourse', [lecturerId, semester, courseId])
        result = [{'Isbn': res[0], 'Title': res[1]} for res in cursor.fetchall()]
    return result

def assignTextbook(lecturerId, semester, courseId, textbookIsbn):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerAssignTextbook', [lecturerId, semester, courseId, textbookIsbn])

def unassignTextbook(lecturerId, semester, courseId, textbookIsbn):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerUnassignTextbook', [lecturerId, semester, courseId, textbookIsbn])

def getClassesOfManagedCourse(lecturerId, semester, courseId):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetClassesOfManagedCourse', [lecturerId, semester, courseId])
        result = [res[0] for res in cursor.fetchall()]
    return result

def getManagedClasses(lecturerId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetManagedClasses', [lecturerId, semester])
        result = [res[0] for res in cursor.fetchall()]
    return result

def getStudentsOfManagedClass(lecturerId, classId):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetStudentsOfManagedClass', [lecturerId, classId])
        result = [{'StudentId': res[0], 'StudentName': res[1]} for res in cursor.fetchall()]
    return result

def getNumberOfStudentsOfManagedClass(lecturerId, classId):
    with connection.cursor() as cursor:
        result = 0
        cursor.callproc('lecturerCountStudentsOfManagedClass', [lecturerId, classId, result])
        cursor.execute("SELECT @result")
        result = cursor.fetchone()
    return result

def getTextbooksOfManagedClass(lecturerId, classId):
    with connection.cursor() as cursor:
        cursor.callproc('lecturerGetTextbooksOfManagedClass', [lecturerId, classId])
        result = [{'Isbn': res[0], 'Title': res[1]} for res in cursor.fetchall()]
    return result