from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from attendance.models import Semester, Course, Lecturer, ClassDivided, CollegeDay, Student, Attendance
from attendance.permissions import IsAuthorOrReadOnly
from attendance.serializers import SemesterSerializer, UserSerializer, CourseSerializer, LecturerSerializer, \
    ClassDividedSerializer, CollegeDaySerializer, StudentSerializer, AttendanceSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer


class ClassDividedViewSet(viewsets.ModelViewSet):
    queryset = ClassDivided.objects.all()
    serializer_class = ClassDividedSerializer


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
