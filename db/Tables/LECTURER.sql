USE BKEL;

CREATE TABLE IF NOT EXISTS LECTURER (
    LecturerId DECIMAL(7,0) NOT NULL,
    LecturerName VARCHAR(255) NOT NULL,
    DepartmentNo INTEGER,
    PRIMARY KEY (LecturerId),
    FOREIGN KEY (DepartmentNo) 
        REFERENCES DEPARTMENT(DepartmentNo) 
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

LOAD DATA INFILE '/mnt/DAE242A5E242862B/Code/db/Excel/lecturer.csv' 
INTO TABLE LECTURER
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (LecturerId, LecturerName, DepartmentNo);