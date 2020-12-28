DROP USER IF EXISTS 'office'@'localhost';
CREATE USER 'office'@'localhost' IDENTIFIED BY 'phongdaotao';
GRANT INSERT, DELETE, UPDATE ON BKEL.ATTENDS_CLASS TO 'office'@'localhost';

DROP USER IF EXISTS 'department'@'localhost';
CREATE USER 'department'@'localhost' IDENTIFIED BY 'khoa';
GRANT INSERT, DELETE, UPDATE ON BKEL.CLASS TO 'department'@'localhost';
GRANT INSERT, DELETE, UPDATE ON BKEL.TEACHES TO 'department'@'localhost';

DROP USER IF EXISTS 'lecturer'@'localhost';
CREATE USER 'lecturer'@'localhost' IDENTIFIED BY 'giangvien';
GRANT INSERT, DELETE, UPDATE ON BKEL.ASSIGNS_TEXTBOOK TO 'lecturer'@'localhost';

DROP USER IF EXISTS 'student'@'localhost';
CREATE USER 'student'@'localhost' IDENTIFIED BY 'sinhvien';
GRANT INSERT, DELETE, UPDATE ON BKEL.ENROLLS TO 'student'@'localhost';

GRANT SELECT ON BKEL.* TO 'office'@'localhost', 'department'@'localhost', 'lecturer'@'localhost', 'student'@'localhost';


DROP USER IF EXISTS 'office'@'172.16.6.71';
CREATE USER 'office'@'172.16.6.71' IDENTIFIED BY 'phongdaotao';
GRANT INSERT, DELETE, UPDATE ON BKEL.ATTENDS_CLASS TO 'office'@'172.16.6.71';

DROP USER IF EXISTS 'department'@'172.16.6.71';
CREATE USER 'department'@'172.16.6.71' IDENTIFIED BY 'khoa';
GRANT INSERT, DELETE, UPDATE ON BKEL.CLASS TO 'department'@'172.16.6.71';
GRANT INSERT, DELETE, UPDATE ON BKEL.TEACHES TO 'department'@'172.16.6.71';

DROP USER IF EXISTS 'lecturer'@'172.16.6.71';
CREATE USER 'lecturer'@'172.16.6.71' IDENTIFIED BY 'giangvien';
GRANT INSERT, DELETE, UPDATE ON BKEL.ASSIGNS_TEXTBOOK TO 'lecturer'@'172.16.6.71';

DROP USER IF EXISTS 'student'@'172.16.6.71';
CREATE USER 'student'@'172.16.6.71' IDENTIFIED BY 'sinhvien';
GRANT INSERT, DELETE, UPDATE ON BKEL.ENROLLS TO 'student'@'172.16.6.71';

GRANT SELECT ON BKEL.* TO 'office'@'172.16.6.71', 'department'@'172.16.6.71', 'lecturer'@'172.16.6.71', 'student'@'172.16.6.71';