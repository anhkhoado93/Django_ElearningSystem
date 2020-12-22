from django.db import connection


def getEnrolledCourses(studentId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('studentGetEnrolledCourses', [studentId, semester])
        result = [{'CourseId': res[0], 'CourseName': res[1]} for res in cursor.fetchall()]
    return result

def getEnrolledCourseInfo(studentId, courseId, semester):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('studentGetAssignedClassOfEnrolledCourse', [studentId, semester, courseId])
            assigned_class = cursor.fetchone()
        with connection.cursor() as cursor:
            cursor.callproc('studentGetLecturersOfAssignedClass', [studentId, assigned_class])
            lecturers = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.callproc('studentGetTextbooksOfEnrolledCourse', [studentId, semester, courseId])
            textbooks = cursor.fetchall()
        result = {
            'CourseId': courseId, 
            'ClassId': assigned_class,
            'Lecturers': [res[0] for res in lecturers],
            'Textbooks': [res[1] for res in textbooks]
        }
        return result
    except:
        raise Exception(f"You didn\'t enroll this course in semester {semester}.")

def getOpenedCourses(semester):
    with connection.cursor() as cursor:
        cursor.callproc('studentGetOpenedCourses', [semester])
        result = [{'CourseId': res[0], 'CourseName': res[1], 'Credits': res[2]} for res in cursor.fetchall()]
    return result

def registerCourse(studentId, courseId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('studentEnrollCourse', [studentId, semester, courseId])

def cancelCourse(studentId, courseId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('studentCancelCourse', [studentId, semester, courseId])

def getTotalCredits(studentId, semester):
    with connection.cursor() as cursor:
        result = 0
        cursor.callproc('studentCountEnrolledCredits', [studentId, semester, result])
    return result

def getTotalEnrolledCourses(studentId, semester):
    with connection.cursor() as cursor:
        result = 0
        cursor.callproc('studentCountEnrolledCourses', [studentId, semester, result])
    return result
