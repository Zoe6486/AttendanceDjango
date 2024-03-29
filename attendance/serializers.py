from django.contrib.auth.models import User
from rest_framework import serializers

from attendance.models import Semester, Course, Lecturer, ClassDivided, CollegeDay, Student, Attendance


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        # extra_kwargs = {'password': {'write_only': True, "required": False}}


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['staff_id', 'username', 'first_name', 'last_name', 'email', 'dob', 'user']


class ClassDividedSerializer(serializers.ModelSerializer):
    semester = serializers.StringRelatedField()  # Use StringRelatedField to represent related model as string
    course = serializers.StringRelatedField()
    class_number = serializers.IntegerField()
    lecturer = serializers.StringRelatedField()
    class Meta:
        model = ClassDivided
        fields = ['id', 'semester', 'course', 'class_number', 'lecturer']


class CollegeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDay
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'username', 'first_name', 'last_name', 'email', 'dob', 'enrolled_classes', 'user']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
