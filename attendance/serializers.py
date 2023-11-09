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
        fields = ["id", "username", "password"]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = "__all__"


class ClassDividedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDivided
        fields = "__all__"


class CollegeDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDay
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
