# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AssignsTextbook(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    semester = models.IntegerField(db_column='Semester')  # Field name made lowercase.
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='CourseId')  # Field name made lowercase.
    textbookid = models.ForeignKey('Textbook', models.DO_NOTHING, db_column='TextbookId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ASSIGNS_TEXTBOOK'
        unique_together = (('semester', 'courseid', 'textbookid'),)


class AttendsClass(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    classid = models.ForeignKey('Class', models.DO_NOTHING, db_column='ClassId')  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='StudentId')  # Field name made lowercase.
    result = models.JSONField(db_column='Result', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ATTENDS_CLASS'
        unique_together = (('classid', 'studentid'),)


class Author(models.Model):
    authorid = models.AutoField(db_column='AuthorId', primary_key=True)  # Field name made lowercase.
    authorname = models.CharField(db_column='AuthorName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AUTHOR'


class Class(models.Model):
    semester = models.IntegerField(db_column='Semester')  # Field name made lowercase.
    classid = models.CharField(db_column='ClassId', primary_key=True, max_length=255)  # Field name made lowercase.
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='CourseId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CLASS'


class Course(models.Model):
    courseid = models.CharField(db_column='CourseId', primary_key=True, max_length=6)  # Field name made lowercase.
    coursename = models.CharField(db_column='CourseName', max_length=255)  # Field name made lowercase.
    departmentno = models.ForeignKey('Department', models.DO_NOTHING, db_column='DepartmentNo')  # Field name made lowercase.
    credits = models.JSONField(db_column='Credits')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COURSE'


class Department(models.Model):
    departmentno = models.AutoField(db_column='DepartmentNo', primary_key=True)  # Field name made lowercase.
    departmentname = models.CharField(db_column='DepartmentName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DEPARTMENT'


class Enrolls(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    semester = models.IntegerField(db_column='Semester')  # Field name made lowercase.
    studentid = models.ForeignKey('Student', models.DO_NOTHING, db_column='StudentId')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='CourseId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENROLLS'
        unique_together = (('semester', 'studentid', 'courseid'),)


class Lecturer(models.Model):
    lecturerid = models.DecimalField(db_column='LecturerId', primary_key=True, max_digits=7, decimal_places=0)  # Field name made lowercase.
    lecturername = models.CharField(db_column='LecturerName', max_length=255)  # Field name made lowercase.
    departmentno = models.ForeignKey(Department, models.DO_NOTHING, db_column='DepartmentNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LECTURER'


class ManagesClass(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='ClassId')  # Field name made lowercase.
    lecturerid = models.ForeignKey(Lecturer, models.DO_NOTHING, db_column='LecturerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MANAGES_CLASS'
        unique_together = (('classid', 'lecturerid'),)


class ManagesCourse(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    semester = models.IntegerField(db_column='Semester')  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='CourseId')  # Field name made lowercase.
    lecturerid = models.ForeignKey(Lecturer, models.DO_NOTHING, db_column='LecturerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MANAGES_COURSE'
        unique_together = (('semester', 'courseid'),)


class Publisher(models.Model):
    publisherid = models.AutoField(db_column='PublisherId', primary_key=True)  # Field name made lowercase.
    publishername = models.CharField(db_column='PublisherName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBLISHER'


class Publishes(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    textbookid = models.OneToOneField('Textbook', models.DO_NOTHING, db_column='TextbookId')  # Field name made lowercase.
    publisherid = models.ForeignKey(Publisher, models.DO_NOTHING, db_column='PublisherId')  # Field name made lowercase.
    publisheddate = models.DateTimeField(db_column='PublishedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUBLISHES'


class Student(models.Model):
    studentid = models.DecimalField(db_column='StudentId', primary_key=True, max_digits=7, decimal_places=0)  # Field name made lowercase.
    studentname = models.CharField(db_column='StudentName', max_length=255)  # Field name made lowercase.
    currentstatus = models.CharField(db_column='CurrentStatus', max_length=9)  # Field name made lowercase.
    departmentno = models.ForeignKey(Department, models.DO_NOTHING, db_column='DepartmentNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'STUDENT'


class Teaches(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    week = models.IntegerField(db_column='Week')  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='ClassId')  # Field name made lowercase.
    lecturerid = models.ForeignKey(Lecturer, models.DO_NOTHING, db_column='LecturerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEACHES'
        unique_together = (('week', 'classid', 'lecturerid'),)


class Textbook(models.Model):
    isbn = models.DecimalField(db_column='Isbn', primary_key=True, max_digits=13, decimal_places=0)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    field = models.CharField(db_column='Field', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEXTBOOK'


class Uses(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='CourseId')  # Field name made lowercase.
    textbookid = models.ForeignKey(Textbook, models.DO_NOTHING, db_column='TextbookId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USES'
        unique_together = (('courseid', 'textbookid'),)


class Writes(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    textbookid = models.ForeignKey(Textbook, models.DO_NOTHING, db_column='TextbookId')  # Field name made lowercase.
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WRITES'
        unique_together = (('textbookid', 'authorid'),)