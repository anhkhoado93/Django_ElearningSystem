USE BKEL;

CREATE TABLE IF NOT EXISTS COURSE (
    CourseId CHAR(6) NOT NULL,
    CourseName VARCHAR(255) NOT NULL,
    DepartmentNo INTEGER NOT NULL,
    Credits INTEGER NOT NULL CHECK (Credits > 0 AND Credits < 4),
    PRIMARY KEY (CourseId),
    FOREIGN KEY (DepartmentNo) 
        REFERENCES DEPARTMENT(DepartmentNo)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

LOAD DATA INFILE '/mnt/DAE242A5E242862B/Code/db/Excel/course.csv' 
INTO TABLE COURSE
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (CourseId, CourseName, DepartmentNo, Credits);