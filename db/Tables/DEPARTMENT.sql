-- DROP DATABASE BKEL;
-- CREATE DATABASE BKEL;

USE BKEL;

CREATE TABLE IF NOT EXISTS DEPARTMENT (
    DepartmentNo INTEGER NOT NULL AUTO_INCREMENT,
    DepartmentName VARCHAR(255) NOT NULL,
    UNIQUE (DepartmentName),
    PRIMARY KEY (DepartmentNo)
);

LOAD DATA INFILE '/mnt/DAE242A5E242862B/Code/db/Excel/department.csv' 
INTO TABLE DEPARTMENT
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (DepartmentNo, DepartmentName);