USE BKEL;

CREATE TABLE IF NOT EXISTS STUDENT (
    StudentId DECIMAL(7,0) NOT NULL,
    StudentName VARCHAR(255) NOT NULL,
    CurrentStatus ENUM('Active','Suspended','Expeled') NOT NULL,
    DepartmentNo INTEGER,
    PRIMARY KEY (StudentId),
    FOREIGN KEY (DepartmentNo) 
        REFERENCES DEPARTMENT(DepartmentNo) 
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

LOAD DATA INFILE '/mnt/DAE242A5E242862B/Code/db/Excel/student.csv' 
INTO TABLE STUDENT
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (StudentId, StudentName, CurrentStatus, DepartmentNo);