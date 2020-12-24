from django.db import connection


def openClass(departmentId, semester, courseId):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT ClassId FROM CLASS WHERE Semester = '{semester}' AND CourseId = '{courseId}' ORDER BY ClassId DESC LIMIT 1")
        res = cursor.fetchone()[0]
        classId = res[:-1] + str(int(res[-1])+1)
    with connection.cursor() as cursor:
        cursor.callproc('departmentOpenClassOfCourse', [departmentId, semester, courseId, classId])

def closeClass(departmentId, semester, courseId, classId):
    with connection.cursor() as cursor:
        cursor.callproc('departmentCloseClassOfCourse', [departmentId, semester, courseId, classId])

def assignLecturerToClass(departmentId, classId, lecturerId):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT Week FROM TEACHES WHERE ClassId = '{classId}' ORDER BY Week LIMIT 1")
        res = cursor.fetchone()
        week = res[0] + 1 if res else 1
    with connection.cursor() as cursor:
        cursor.callproc('departmentAssignLecturerOfClass', [departmentId, week, classId, lecturerId])

def getOpenedCourses(departmentId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('departmentGetOpenedCourses', [departmentId, semester])
        result = [{'CourseId': res[0], 'CourseName': res[1]} for res in cursor.fetchall()]
    return result

def getClassesOfCourse(departmentId, semester, courseId):
    with connection.cursor() as cursor:
        cursor.callproc('departmentGetClassesOfCourse', [departmentId, semester, courseId])
        result = [res[0] for res in cursor.fetchall()]
    return result

def getWorkingLecturers(departmentId, semester):
    with connection.cursor() as cursor:
        cursor.callproc('departmentGetWorkingLecturers', [departmentId, semester])
        result = [{'LecturerId': res[0], 'LecturerName': res[1]} for res in cursor.fetchall()]
    return result

def getTextbooksOfCourse(departmentId, semester, courseId):
    with connection.cursor() as cursor:
        cursor.callproc('departmentGetTextbooksOfCourse', [departmentId, semester, courseId])
        result = [{'Isbn': res[0], 'Title': res[1]} for res in cursor.fetchall()]
    return result
