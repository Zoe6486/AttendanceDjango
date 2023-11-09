from django.contrib import admin

from attendance.models import Semester, Course, ClassDivided, Lecturer, CollegeDay, Student, Attendance

# Register your models here.
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(ClassDivided)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(CollegeDay)
admin.site.register(Attendance)
