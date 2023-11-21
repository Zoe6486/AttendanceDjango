from django.contrib.auth.models import User
from django.db import models


class Semester(models.Model):
    year = models.PositiveIntegerField()
    semester_str = models.CharField(max_length=255)

    def __str__(self):
        return str(self.year) + " " + self.semester_str


class Course(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.code + " " + self.name


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer")
    staff_id = models.BigIntegerField(primary_key=True, db_column='staff_id', unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.EmailField(null=True, blank=True, default='')
    password = models.CharField(max_length=255, blank=True, null=True, default='')
    dob = models.DateField()

    def __str__(self):
        return str(self.staff_id) + " - " + str(self.first_name) + " " + str(self.last_name)


class ClassDivided(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_number = models.PositiveIntegerField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name="taught_classes")

    def __str__(self):
        return str(self.semester) + " - " + str(self.course) + " - " + "Class " + str(self.class_number)


class CollegeDay(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    is_holiday = models.BooleanField(default=False)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    scheduled_classes = models.ManyToManyField(ClassDivided, blank=True,
                                               related_name="scheduled_collegeDays")

    def __str__(self):
        return str(self.date)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    student_id = models.BigIntegerField(primary_key=True, db_column='student_id', unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.EmailField(null=True)
    password = models.CharField(max_length=255, blank=True, null=True, default='')
    dob = models.DateField()
    enrolled_classes = models.ManyToManyField(ClassDivided, blank=True, related_name="enrolled_students")

    def __str__(self):
        return str(self.student_id) + " - " + str(self.first_name) + " " + str(self.last_name)


class Attendance(models.Model):
    attendance_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name="attendances")
    attendance_day = models.ForeignKey(CollegeDay, on_delete=models.SET_NULL, null=True)
    attendance_class = models.ForeignKey(ClassDivided, on_delete=models.SET_NULL, null=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        if self.is_present:
            str(self.attendance_student) + " is Present"
        else:
            str(self.attendance_student) + " is Absent"

# class ScheduledClass(models.Model):
#     college_day = models.ForeignKey(CollegeDay, on_delete=models.CASCADE)
#     class_name = models.ForeignKey(ClassDivided, on_delete=models.CASCADE, null=True)
#     attended_students = models.ManyToManyField(Student, blank=True,
#                                                related_name="attended_scheduled_classes")
