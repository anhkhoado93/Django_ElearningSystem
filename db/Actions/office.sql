USE BKEL;

DROP PROCEDURE IF EXISTS officeInsertEnrollment;
CREATE PROCEDURE officeInsertEnrollment
    (IN class VARCHAR(255), IN student DECIMAL(7,0))
BEGIN
    DECLARE studentsCount INT UNSIGNED;
    SELECT COUNT(*) INTO studentsCount FROM ATTENDS_CLASS WHERE ClassId = class;
    IF studentsCount = 60 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Each class must have at most 60 students';
    ELSE
        INSERT INTO ATTENDS_CLASS(ClassId, StudentId, Result)
        VALUES (class, student, NULL);
    END IF;
END;

DROP PROCEDURE IF EXISTS officeDeleteEnrollment;
CREATE PROCEDURE officeDeleteEnrollment
    (IN class VARCHAR(255), IN student DECIMAL(7,0))
BEGIN
    DELETE FROM ATTENDS_CLASS
    WHERE ClassId = class AND StudentId = student;
END;

DROP PROCEDURE IF EXISTS officeGetUnassignedEnrollment;
CREATE PROCEDURE officeGetUnassignedEnrollment
    (IN semester INTEGER)
BEGIN
    SELECT E.StudentId, E.CourseId
    FROM CLASS AS CL
    JOIN ATTENDS_CLASS AS A
    ON CL.ClassId = A.ClassId
    RIGHT JOIN ENROLLS AS E
    ON CL.CourseId = E.CourseId
        AND CL.Semester = E.Semester
        AND A.StudentId = E.StudentId
    WHERE E.Semester = semester
        AND A.ClassId IS NULL;
END;

DROP PROCEDURE IF EXISTS officeGetEnrolledClassesOfStudent;
CREATE PROCEDURE officeGetEnrolledClassesOfStudent
    (IN student DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT C.CourseId, C.CourseName, A.ClassId
    FROM ATTENDS_CLASS AS A
    JOIN CLASS AS CL
    ON A.ClassId = CL.ClassId
        AND CL.Semester = semester
        AND A.StudentId = student
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId;
END;

DROP PROCEDURE IF EXISTS officeGetManagedClassesOfLecturer;
CREATE PROCEDURE officeGetManagedClassesOfLecturer
    (IN lecturer DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT DISTINCT C.CourseId, C.CourseName, M.ClassId
    FROM MANAGES_CLASS AS M
    JOIN CLASS AS CL
    ON M.ClassId = CL.ClassId
        AND CL.Semester = semester
    JOIN COURSE AS C
    ON M.CourseId = C.CourseId
        AND M.LecturerId = lecturer;
END;

DROP PROCEDURE IF EXISTS officeGetEnrolledCoursesOfDepartments;
CREATE PROCEDURE officeGetEnrolledCoursesOfDepartments()
BEGIN
    SELECT DISTINCT D.DepartmentName, E.Semester, C.CourseId, C.CourseName
    FROM ENROLLS AS E
    JOIN COURSE AS C
    ON E.CourseId = C.CourseId
    JOIN DEPARTMENT AS D
    ON C.DepartmentNo = D.DepartmentNo
    ORDER BY D.DepartmentNo, E.Semester DESC, C.CourseId, C.CourseName;
END;

DROP PROCEDURE IF EXISTS officeGetStudentsInClasses;
CREATE PROCEDURE officeGetStudentsInClasses()
BEGIN
    SELECT D.DepartmentName, CL.Semester, C.CourseId, C.CourseName, CL.ClassId, A.StudentId, S.StudentName
    FROM ATTENDS_CLASS AS A
    JOIN CLASS AS CL
    ON A.ClassId = CL.ClassId
    JOIN STUDENT AS S
    ON A.StudentId = S.StudentId
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId
    JOIN DEPARTMENT AS D
    ON C.DepartmentNo = D.DepartmentNo
    ORDER BY D.DepartmentNo, CL.Semester DESC, C.CourseId, CL.ClassId, A.StudentId;
END;

DROP PROCEDURE IF EXISTS officeGetLecturersInClasses;
CREATE PROCEDURE officeGetLecturersInClasses()
BEGIN
    SELECT DISTINCT D.DepartmentName, T.Semester, C.CourseName, T.ClassId, L.LecturerId, L.LecturerName
    FROM TEACHES AS T
    JOIN LECTURER AS L
    ON T.LecturerId = L.LecturerId
    JOIN COURSE AS C
    ON T.CourseId = C.CourseId
    JOIN DEPARTMENT AS D
    ON C.DepartmentNo = D.DepartmentNo
    ORDER BY D.DepartmentNo, T.Semester DESC, T.CourseId, T.ClassId, T.LecturerNo;
END;

DROP PROCEDURE IF EXISTS officeGetTextbooksOfCourses;
CREATE PROCEDURE officeGetTextbooksOfCourses()
BEGIN
    SELECT A.Semester, C.CourseName, T.Title
    FROM ASSIGNS_TEXTBOOK AS A
    JOIN TEXTBOOK AS T
    ON A.TextbookId = T.Isbn
    JOIN COURSE AS C
    ON A.CourseId = C.CourseId
    ORDER BY A.Semester, A.CourseId;
END;

DROP PROCEDURE IF EXISTS officeCountCoursesOfDepartments;
CREATE PROCEDURE officeCountCoursesOfDepartments()
BEGIN
    SELECT D.DepartmentName, E.Semester, COUNT(DISTINCT E.CourseId) AS 'CoursesCount'
    FROM ENROLLS AS E
    JOIN COURSE AS C
    ON E.CourseId = C.CourseId
    JOIN DEPARTMENT AS D
    ON C.DepartmentNo = D.DepartmentNo
    GROUP BY D.DepartmentNo, E.Semester
    ORDER BY D.DepartmentNo, E.Semester DESC;
END;

DROP PROCEDURE IF EXISTS officeCountClassesOfDepartments;
CREATE PROCEDURE officeCountClassesOfDepartments()
BEGIN
    SELECT D.DepartmentName, CL.Semester, COUNT(CL.ClassId) AS 'ClassesCount'
    FROM CLASS AS CL
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId
    JOIN DEPARTMENT AS D
    ON C.DepartmentNo = D.DepartmentNo
    GROUP BY D.DepartmentNo, CL.Semester
    ORDER BY D.DepartmentNo, CL.Semester DESC;
END;

DROP PROCEDURE IF EXISTS officeCountStudentsInClasses;
CREATE PROCEDURE officeCountStudentsInClasses
    (IN course CHAR(6), IN semester INTEGER)
BEGIN
    SELECT A.ClassId, COUNT(A.StudentId) AS 'StudentsCount'
    FROM ATTENDS_CLASS AS A
    WHERE A.Semester = semester AND A.CourseId = course
    GROUP BY A.ClassId;
END;

DROP PROCEDURE IF EXISTS officeCountStudentsOfCourses;
CREATE PROCEDURE officeCountStudentsOfCourses
    (IN semester INTEGER)
BEGIN
    SELECT C.CourseId, C.CourseName, COUNT(E.StudentNo) AS 'StudentsCount'
    FROM ENROLLS AS E
    JOIN COURSE AS C
    ON E.CourseId = C.CourseId AND E.Semester = semester
    GROUP BY E.CourseId;
END;

DROP PROCEDURE IF EXISTS officeCountStudentsOfDepartments;
CREATE PROCEDURE officeCountStudentsOfDepartments
    (IN department INTEGER)
BEGIN
    SELECT E.Semester, COUNT(DISTINCT E.StudentNo) AS 'StudentsCount'
    FROM ENROLLS AS E
    JOIN STUDENT AS S
    ON E.StudentId = S.StudentId
    JOIN DEPARTMENT AS D
    ON S.DepartmentNo = D.DepartmentNo 
        AND D.DepartmentNo = department
    GROUP BY E.Semester
    ORDER BY E.Semester DESC;
END;