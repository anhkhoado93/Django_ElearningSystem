USE BKEL;

DROP PROCEDURE IF EXISTS lecturerAssignTextbook;
CREATE PROCEDURE lecturerAssignTextbook
    (IN lecturer DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6), IN textbook DECIMAL(13,0))
BEGIN
    IF (SELECT COUNT(*) FROM MANAGES_COURSE WHERE LecturerId = lecturer AND CourseId = course AND Semester = semester) > 0 THEN
        IF (SELECT COUNT(*) FROM USES WHERE CourseId = course AND TextbookId = textbook) THEN
            INSERT INTO ASSIGNS_TEXTBOOK(Semester, CourseId, TextbookId)
            VALUES (semester, course, textbook);
        ELSE
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Textbook is not appropriate for this subject';
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You are not managing this course';
    END IF;
END;

DROP PROCEDURE IF EXISTS lecturerUnassignTextbook;
CREATE PROCEDURE lecturerUnassignTextbook
    (IN lecturer DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6), IN textbook DECIMAL(13,0))
BEGIN
    IF (SELECT COUNT(*) FROM MANAGES_COURSE WHERE LecturerId = lecturer AND CourseId = course AND Semester = semester) > 0 THEN
        DELETE FROM ASSIGNS_TEXTBOOK
        WHERE Semester = semester AND CourseId = course AND TextbookId = textbook;
    ELSE
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You are not managing this course';
    END IF;
END;

DROP PROCEDURE IF EXISTS lecturerGetManagedCourses;
CREATE PROCEDURE lecturerGetManagedCourses
    (IN lecturer DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT C.CourseId, C.CourseName
    FROM MANAGES_COURSE AS M
    JOIN COURSE AS C
    ON M.CourseId = C.CourseId
        AND M.Semester = semester
        AND M.LecturerId = lecturer;
END;

DROP PROCEDURE IF EXISTS lecturerGetUsedTextbooksOfManagedCourse;
CREATE PROCEDURE lecturerGetUsedTextbooksOfManagedCourse
    (IN course CHAR(6))
BEGIN
    SELECT T.Isbn, T.Title
    FROM USES AS U
    JOIN TEXTBOOK AS T
    ON U.TextbookId = T.Isbn
        AND U.CourseId = course;
END;

DROP PROCEDURE IF EXISTS lecturerGetTextbooksOfManagedCourse;
CREATE PROCEDURE lecturerGetTextbooksOfManagedCourse
    (IN lecturer DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    SELECT T.Isbn, T.Title
    FROM MANAGES_COURSE AS M
    JOIN ASSIGNS_TEXTBOOK AS A
    ON M.CourseId = A.CourseId
        AND M.Semester = A.Semester
        AND M.Semester = semester
        AND M.LecturerId = lecturer
    JOIN TEXTBOOK AS T
    ON A.TextbookId = T.Isbn;
END;

DROP PROCEDURE IF EXISTS lecturerGetClassesOfManagedCourse;
CREATE PROCEDURE lecturerGetClassesOfManagedCourse
    (IN lecturer DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    SELECT CL.ClassId
    FROM MANAGES_COURSE AS M
    JOIN CLASS AS CL
    ON M.CourseId = CL.CourseId
        AND M.Semester = CL.Semester
        AND M.Semester = semester
        AND M.LecturerId = lecturer
        AND M.CourseId = course;
END;

DROP PROCEDURE IF EXISTS lecturerGetManagedClasses;
CREATE PROCEDURE lecturerGetManagedClasses
    (IN lecturer DECIMAL(7,0), In semester INTEGER)
BEGIN
    SELECT T.Week, CL.ClassId
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClassId = CL.ClassId
        AND CL.Semester = semester
        AND T.LecturerId = lecturer;
END;

DROP PROCEDURE IF EXISTS lecturerGetStudentsOfManagedClass;
CREATE PROCEDURE lecturerGetStudentsOfManagedClass
    (IN lecturer DECIMAL(7,0), IN class VARCHAR(255))
BEGIN
    SELECT DISTINCT S.StudentId, S.StudentName
    FROM TEACHES AS T
    JOIN ATTENDS_CLASS AS A
    ON A.ClassId = T.ClassId
        AND T.LecturerId = lecturer
        AND T.ClassId = class
    JOIN STUDENT AS S
    ON A.StudentId = S.StudentId;
END;

DROP PROCEDURE IF EXISTS lecturerCountStudentsOfManagedClass;
CREATE PROCEDURE lecturerCountStudentsOfManagedClass
    (IN lecturer DECIMAL(7,0), IN class VARCHAR(255), OUT total INTEGER)
BEGIN
    SELECT COUNT(DISTINCT A.StudentId) AS 'StudentsCount'
    INTO total
    FROM TEACHES AS T
    JOIN ATTENDS_CLASS AS A
    ON A.ClassId = T.ClassId
        AND T.ClassId = class
        AND T.LecturerId = lecturer;
END;

DROP PROCEDURE IF EXISTS lecturerGetTextbooksOfManagedClass;
CREATE PROCEDURE lecturerGetTextbooksOfManagedClass
    (IN lecturer DECIMAL(7,0), IN class VARCHAR(255))
BEGIN
    SELECT DISTINCT TB.Isbn, TB.Title
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClassId = CL.ClassId
        AND T.LecturerId = lecturer
    JOIN ASSIGNS_TEXTBOOK AS A
    ON CL.CourseId = A.CourseId
        AND CL.Semester = A.Semester
    JOIN TEXTBOOK AS TB
    ON A.TextbookId = TB.Isbn;
END;

DROP PROCEDURE IF EXISTS lecturerCountManagedClassesInThreeYears;
CREATE PROCEDURE lecturerCountManagedClassesInThreeYears
    (IN lecturer DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT CL.Semester, COUNT(DISTINCT T.ClassId) AS 'ClassesCount'
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON CL.Semester >= semester-30
        AND T.LecturerId = lecturer
    GROUP BY CL.Semester
    ORDER BY CL.Semester DESC;
END;

DROP PROCEDURE IF EXISTS lecturerGetFiveManagedClassesOfMostStudents;
CREATE PROCEDURE lecturerGetFiveManagedClassesOfMostStudents
    (IN lecturer DECIMAL(7,0))
BEGIN
    SELECT DISTINCT CL.Semester, CL.CourseId, C.CourseName, CL.ClassId, COUNT(A.StudentId) AS 'StudentsCount'
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClasId = CL.ClassId
        AND CL.Semester = semester
        AND T.LecturerId = lecturer
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId
    JOIN ATTENDS_CLASS AS A
    ON A.ClassId = CL.ClassId
    GROUP BY CL.Semester, CL.CourseId, CL.ClassId
    ORDER BY 'StudentsCount' DESC
    LIMIT 5;
END;

DROP PROCEDURE IF EXISTS lecturerGetFiveSemestersOfMostManagedClasses;
CREATE PROCEDURE lecturerGetFiveSemestersOfMostManagedClasses
    (IN lecturer DECIMAL(7,0))
BEGIN
    SELECT CL.Semester, COUNT(DISTINCT T.ClassId) AS 'ClassesCount'
    FROM TEACHES AS T
    JOIN CLASS AS CL
    ON T.ClassId = CL.ClassId
        AND T.LecturerId = lecturer
    GROUP BY CL.Semester
    ORDER BY 'ClassesCount' DESC
    LIMIT 5;
END;