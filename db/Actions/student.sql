USE BKEL;

DROP PROCEDURE IF EXISTS studentEnrollCourse;
CREATE PROCEDURE studentEnrollCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    DECLARE currentCredits INT UNSIGNED;
    DECLARE courseCredits INT UNSIGNED;
    CALL studentCountEnrolledCredits(student, semester, currentCredits);
    SELECT credits INTO courseCredits FROM COURSE WHERE CourseId = course;
    IF currentCredits + courseCredits > 18 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You cannot enroll more than 18 credits in a semester.';
    ELSE
        INSERT INTO ENROLLS(Semester, StudentId, CourseId)
        VALUES (semester, student, course);
    END IF;
END;

DROP PROCEDURE IF EXISTS studentCancelCourse;
CREATE PROCEDURE studentCancelCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    DELETE FROM ENROLLS
    WHERE Semester = semester AND StudentId = student AND CourseId = course;
END;

DROP PROCEDURE IF EXISTS studentGetOpenedCourses;
CREATE PROCEDURE studentGetOpenedCourses
    (IN semester INTEGER)
BEGIN
    SELECT DISTINCT C.CourseId, C.CourseName, C.Credits
    FROM CLASS AS CL
    JOIN COURSE AS C
    ON CL.CourseId = C.CourseId
        AND CL.Semester = semester;
END;

DROP PROCEDURE IF EXISTS studentCheckEnrolledCourse;
CREATE PROCEDURE studentCheckEnrolledCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    IF (SELECT COUNT(*) FROM ENROLLS WHERE Semester = semester AND StudentId = student AND CourseId = course) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'You haven''t enrolled this course.';
    END IF;
END;

DROP PROCEDURE IF EXISTS studentGetEnrolledCourses;
CREATE PROCEDURE studentGetEnrolledCourses
    (IN student DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT C.CourseId, C.CourseName
    FROM ENROLLS AS E
    JOIN COURSE AS C
    ON E.CourseId = C.CourseId
        AND E.Semester = semester
        AND E.StudentId = student;
END;

DROP PROCEDURE IF EXISTS studentGetTextbooksOfEnrolledCourse;
CREATE PROCEDURE studentGetTextbooksOfEnrolledCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    CALL studentCheckEnrolledCourse(student, semester, course);
    SELECT T.Isbn, T.Title
    FROM ENROLLS AS E
    JOIN ASSIGNS_TEXTBOOK AS A
    ON E.CourseId = A.CourseId
        AND E.Semester = A.Semester
        AND E.Semester = semester
        AND E.CourseId = course
        AND E.StudentId = student
    JOIN TEXTBOOK AS T
    ON T.Isbn = A.TextbookId;
END;

DROP PROCEDURE IF EXISTS studentGetClassesOfEnrolledCourse;
CREATE PROCEDURE studentGetClassesOfEnrolledCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    CALL studentCheckEnrolledCourse(student, semester, course);
    SELECT CL.ClassId
    FROM ENROLLS AS E
    JOIN CLASS AS CL
    ON E.CourseId = CL.CourseId
        AND E.Semester = semester
        AND E.CourseId = course
        AND E.StudentId = student;
END;

DROP PROCEDURE IF EXISTS studentGetAssignedClassOfEnrolledCourse;
CREATE PROCEDURE studentGetAssignedClassOfEnrolledCourse
    (IN student DECIMAL(7,0), IN semester INTEGER, IN course CHAR(6))
BEGIN
    CALL studentCheckEnrolledCourse(student, semester, course);
    SELECT CL.ClassId
    FROM CLASS AS CL
    JOIN ATTENDS_CLASS AS A
    ON CL.ClassId = A.ClassId
        AND CL.Semester = semester
        AND CL.CourseId = course
        AND A.StudentId = student;
END;

DROP PROCEDURE IF EXISTS studentGetLecturersOfAssignedClass;
CREATE PROCEDURE studentGetLecturersOfAssignedClass
    (IN student DECIMAL(7,0), IN class VARCHAR(255))
BEGIN
    SELECT DISTINCT L.LecturerName
    FROM ATTENDS_CLASS AS A
    JOIN TEACHES AS T
    ON A.ClassId = T.ClassId
        AND A.StudentId = student
        AND A.ClassId = class
    JOIN LECTURER AS L
    ON T.LecturerId = L.LecturerId;
END;

DROP PROCEDURE IF EXISTS studentGetClassesOfEnrolledCoursesWithMoreThanOneLecturer;
CREATE PROCEDURE studentGetClassesOfEnrolledCoursesWithMoreThanOneLecturer
    (IN student DECIMAL(7,0), IN semester INTEGER)
BEGIN
    SELECT C.CourseId, C.CourseName, CL.ClassId, COUNT(DISTINCT T.LecturerNo) AS 'LecturersCount'
    FROM ENROLLS AS E
    JOIN COURSE AS C 
    ON E.CourseId = C.CourseId
        AND E.Semester = semester
        AND E.StudentId = student
    JOIN CLASS AS CL
    ON C.CourseId = CL.CourseId
    JOIN TEACHES AS T
    ON CL.ClassId = T.ClassId
    GROUP BY C.CourseId, CL.ClassId
    HAVING COUNT(DISTINCT T.LecturerId) > 1
    ORDER BY C.CourseId, CL.ClassId;
END;

DROP PROCEDURE IF EXISTS studentCountEnrolledCredits;
CREATE PROCEDURE studentCountEnrolledCredits
    (IN student DECIMAL(7,0), IN semester INTEGER, OUT total INTEGER)
BEGIN
    SELECT SUM(C.Credits)
    INTO total
    FROM ENROLLS AS E
    JOIN COURSE AS C 
    ON E.CourseId = C.CourseId
        AND E.Semester = semester
        AND E.StudentId = student; 
END;

DROP PROCEDURE IF EXISTS studentCountEnrolledCourses;
CREATE PROCEDURE studentCountEnrolledCourses
    (IN student DECIMAL(7,0), IN semester INTEGER, OUT total INTEGER)
BEGIN
    SELECT COUNT(DISTINCT E.CourseId)
    INTO total
    FROM ENROLLS AS E
    WHERE E.Semester = semester
        AND E.StudentId = student;
END;

DROP PROCEDURE IF EXISTS studentGetThreeSemestersWithMostEnrolledCredits;
CREATE PROCEDURE studentGetThreeSemestersWithMostEnrolledCredits
    (IN student DECIMAL(7,0))
BEGIN
    SELECT E.Semester, SUM(Credits) AS 'Total Credits'
    FROM ENROLLS AS E
    JOIN COURSE AS C 
    ON E.CourseId = C.CourseId
        AND E.StudentId = student
    GROUP BY E.Semester
    ORDER BY SUM(Credits) DESC
    LIMIT 3;
END;