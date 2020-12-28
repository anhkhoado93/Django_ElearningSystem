USE BKEL;

DROP PROCEDURE IF EXISTS departmentOpenClassOfCourse;
CREATE PROCEDURE departmentOpenClassOfCourse
    (IN department INTEGER, IN semester INTEGER, IN course CHAR(6), IN class VARCHAR(255))
BEGIN
    IF (SELECT COUNT(*) FROM COURSE WHERE CourseId = course AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This course does not belong to your department.';
    ELSE
        INSERT INTO CLASS(Semester, CourseId, ClassId)
        VALUES (semester, course, class);
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentCloseClassOfCourse;
CREATE PROCEDURE departmentCloseClassOfCourse
    (IN department INTEGER, IN semester INTEGER, IN course CHAR(6), IN class VARCHAR(255))
BEGIN
    IF (SELECT COUNT(*) FROM COURSE WHERE CourseId = course AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This course does not belong to your department.';
    ELSE
        DELETE FROM CLASS
        WHERE ClassId = class;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentAssignLecturerOfClass;
CREATE PROCEDURE departmentAssignLecturerOfClass
    (IN department INTEGER, IN week INTEGER, IN class VARCHAR(255), IN lecturer DECIMAL(7,0))
BEGIN
    IF (SELECT COUNT(*) FROM LECTURER WHERE LecturerId = lecturer AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This lecturer does not belong to your department.';
    ELSE
        IF (SELECT COUNT(*) FROM CLASS AS CL JOIN COURSE AS C ON CL.CourseId = C.CourseId AND C.DepartmentNo = department) = 0 THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'This class does not belong to your department.';
        ELSE
            INSERT INTO TEACHES(Week, ClassId, LecturerId)
            VALUES (week, class, lecturer);
        END IF;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentGetOpenedCourses;
CREATE PROCEDURE departmentGetOpenedCourses
    (IN department INTEGER, IN semester INTEGER)
BEGIN
    SELECT DISTINCT C.CourseId, C.CourseName
    FROM CLASS AS CL
    JOIN COURSE AS C 
    ON CL.CourseId = C.CourseId 
        AND CL.Semester = semester
        AND C.DepartmentNo = department;
END;

DROP PROCEDURE IF EXISTS departmentGetClassesOfCourse;
CREATE PROCEDURE departmentGetClassesOfCourse
    (IN department INTEGER, IN semester INTEGER, IN course CHAR(6))
BEGIN
    IF (SELECT COUNT(*) FROM COURSE WHERE CourseId = course AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This course does not belong to your department.';
    ELSE
        SELECT CL.ClassId
        FROM CLASS AS CL
        JOIN COURSE AS C
        ON CL.CourseId = C.CourseId 
            AND CL.Semester = semester
            AND C.DepartmentNo = department
            AND C.CourseId = course;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentGetWorkingLecturers;
CREATE PROCEDURE departmentGetWorkingLecturers
    (IN department INTEGER, IN semester INTEGER)
BEGIN
    SELECT DISTINCT L.LecturerId, L.LecturerName
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClassId = CL.ClassId
        AND CL.Semester = semester
    JOIN LECTURER AS L
    ON T.LecturerId = L.LecturerId 
        AND L.DepartmentNo = department;
END;

DROP PROCEDURE IF EXISTS departmentGetClassesOfLecturer;
CREATE PROCEDURE departmentGetClassesOfLecturer
    (IN department INTEGER, IN lecturer DECIMAL(7,0), IN semester INTEGER)
BEGIN
    IF (SELECT COUNT(*) FROM LECTURER WHERE LecturerId = lecturer AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This lecturer does not belong to your department.';
    ELSE
        SELECT DISTINCT C.CourseId, C.CourseName, T.ClassId
        FROM TEACHES AS T
        JOIN CLASS AS CL
        ON T.ClassId = CL.ClassId
        JOIN COURSE AS C
        ON CL.CourseId = C.CourseId
        JOIN LECTURER AS L
        ON T.LecturerId = L.LecturerId
            AND L.LecturerId = lecturer
            AND T.Semester = semester;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentGetLecturersOfClass;
CREATE PROCEDURE departmentGetLecturersOfClass
    (IN department INTEGER, IN semester INTEGER, IN class VARCHAR(255))
BEGIN
    IF (SELECT COUNT(*) FROM CLASS AS CL JOIN COURSE AS C ON CL.CourseId = C.CourseId AND C.DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This class does not belong to your department.';
    ELSE
        SELECT T.Week, L.LecturerId, L.LecturerName
        FROM TEACHES AS T
        JOIN LECTURER AS L
        ON T.LecturerId = L.LecturerId
            AND T.ClassId = class
        ORDER BY T.Week;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentGetTextbooksOfCourse;
CREATE PROCEDURE departmentGetTextbooksOfCourse
    (IN department INTEGER, IN semester INTEGER, IN course CHAR(6))
BEGIN
    IF (SELECT COUNT(*) FROM COURSE WHERE CourseId = course AND DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This course does not belong to your department.';
    ELSE
        SELECT T.Title
        FROM ASSIGNS_TEXTBOOK AS A
        JOIN TEXTBOOK AS T
        ON A.TextbookId = T.Isbn 
            AND A.Semester = semester
            AND A.CourseId = course;
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentGetStudentsOfClass;
CREATE PROCEDURE departmentGetStudentsOfClass
    (IN department INTEGER, IN semester INTEGER, IN class VARCHAR(255))
BEGIN
    IF (SELECT COUNT(*) FROM CLASS AS CL JOIN COURSE AS C ON CL.CourseId = C.CourseId AND C.DepartmentNo = department) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'This class does not belong to your department.';
    ELSE
        SELECT S.StudentId, S.StudentName
        FROM ATTENDS_CLASS AS A
        JOIN CLASS AS CL
        ON A.ClassId = CL.ClassId
            AND A.Semester = semester
            AND A.ClassId = class
        JOIN STUDENT AS S
        ON A.StudentId = S.StudentId; 
    END IF;
END;

DROP PROCEDURE IF EXISTS departmentCountStudentsOfCourse;
CREATE PROCEDURE departmentCountStudentsOfCourse
    (IN semester INTEGER)
BEGIN
    SELECT COUNT(DISTINCT E.StudentNo) AS 'StudentsCount'
    FROM ENROLLS AS E
    WHERE E.Semester = semester;
END;

DROP PROCEDURE IF EXISTS departmentCountClasses;
CREATE PROCEDURE departmentCountClasses
    (IN semester INTEGER)
BEGIN
    SELECT COUNT(C.ClassId) AS 'ClassesCount'
    FROM CLASS AS CL
    WHERE CL.Semester = semester;
END;

DROP PROCEDURE IF EXISTS departmentGetCoursesOfMostLecturers;
CREATE PROCEDURE departmentGetCoursesOfMostLecturers
    (IN semester INTEGER)
BEGIN
    SELECT C.CourseName, COUNT(DISTINCT T.LecturerId) AS 'LecturersCount'
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClassId = CL.ClassId
        AND CL.Semester = semester
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId
    GROUP BY T.CourseId
    HAVING 'LecturersCount' = MAX('LecturersCount');
END;

DROP PROCEDURE IF EXISTS departmentGetAverageStudentsInThreeYears;
CREATE PROCEDURE departmentGetAverageStudentsInThreeYears
    (IN course CHAR(6), IN semester INTEGER)
BEGIN
    SELECT AVG(S.StudentCount)
    FROM (
        SELECT E.Semester, COUNT(E.StudentId) AS 'StudentCount'
        FROM ENROLLS AS E
        WHERE E.CourseId = course 
            AND E.Semester >= semester-30
        GROUP BY E.Semester
    ) AS S;
END;