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
        pass