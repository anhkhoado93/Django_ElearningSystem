from django.db import connection


def getUnassignedEnrollment(semester):
    with connection.cursor() as cursor:
        cursor.callproc('officeGetUnassignedEnrollment', [semester])
        result = [{'StudentId': res[0], 'CourseId': res[1]} for res in cursor.fetchall()]
    return result

def assignEnrollment(studentId, classId):
    with connection.cursor() as cursor:
        cursor.callproc('officeInsertEnrollment', [classId, studentId])

def unassignEnrollment(studentId, classId):
    with connection.cursor() as cursor:
        cursor.callproc('officeDeleteEnrollment', [classId, studentId])

def getDepartments():
    with connection.cursor() as cursor:
        SQLcommand = "SELECT * FROM DEPARTMENT"
        cursor.execute(SQLcommand)
        result = [{'DepartmentId': res[0], 'DepartmentName': res[1]} for res in cursor.fetchall()]
    return result

def getCoursesOfDepartment(department):
    with connection.cursor() as cursor:
        SQLcommand = f"SELECT CourseId, CourseName FROM COURSE WHERE DepartmentNo = {department}"
        cursor.execute(SQLcommand)
        result = [{'CourseId': res[0], 'CourseName': res[1]} for res in cursor.fetchall()]
    return result

def getClassesOfCourse(semester, courseId):
    with connection.cursor() as cursor:
        SQLcommand = f"SELECT ClassId FROM CLASS WHERE Semester = {semester} AND CourseId = '{courseId}'"
        cursor.execute(SQLcommand)
        result = [res[0] for res in cursor.fetchall()]
    return result

def getStudentsOfClass(classId):
    with connection.cursor() as cursor:
        SQLcommand = f"SELECT S.StudentId, S.StudentName FROM ATTENDS_CLASS AS A JOIN STUDENT AS S ON A.StudentId = S.StudentId AND A.ClassId = '{classId}'"
        cursor.execute(SQLcommand)
        result = [{'StudentId': res[0], 'StudentName': res[1]} for res in cursor.fetchall()]
    return result

def getLecturersOfClass(classId):
    with connection.cursor() as cursor:
        SQLcommand = f"SELECT DISTINCT L.LecturerId, L.LecturerName FROM TEACHES AS T JOIN LECTURER AS L ON T.LecturerId = L.LecturerId AND T.ClassId = '{classId}'"
        cursor.execute(SQLcommand)
        result = [{'LecturerId': res[0], 'LecturerName': res[1]} for res in cursor.fetchall()]
    return result