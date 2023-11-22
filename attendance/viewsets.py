from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from attendance.models import Semester, Course, Lecturer, ClassDivided, CollegeDay, Student, Attendance
from attendance.permissions import IsAuthorOrReadOnly
from attendance.serializers import SemesterSerializer, UserSerializer, CourseSerializer, LecturerSerializer, \
    ClassDividedSerializer, CollegeDaySerializer, StudentSerializer, AttendanceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = (AllowAny,)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (AllowAny,)


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Extract user-related data from the request
        username = request.data.get('username')  # You can customize this as needed
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Create the user
        user, created = User.objects.get_or_create(username=username,
                                                   defaults={'email': email, 'password': make_password(password),
                                                             'first_name': first_name, 'last_name': last_name})

        # Add the user to the "lecturer_user" group if needed
        lecturer_group, created = Group.objects.get_or_create(name='lecturer_user')
        user.groups.add(lecturer_group)

        request.data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        user.set_password(password)
        user.save()

        lecturer_data = {
            'staff_id': request.data.get('staff_id'),
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'dob': request.data.get('dob'),
            'user': user.id
        }

        lecturer_serializer = LecturerSerializer(data=lecturer_data)
        if lecturer_serializer.is_valid():
            lecturer_serializer.save()
            return Response(lecturer_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(lecturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        # Refresh the user instance from the database to get the latest changes
        user.refresh_from_db()

        # Update User object
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        password = request.data.get('password')
        if password:
            user.set_password(password)
        user.save()

        # Update Lecturer object
        lecturer_data = {
            'staff_id': request.data.get('staff_id', instance.staff_id),
            'username': request.data.get('username', instance.username),
            'first_name': request.data.get('first_name', instance.first_name),
            'last_name': request.data.get('last_name', instance.last_name),
            'email': request.data.get('email', instance.email),
            'dob': request.data.get('dob', instance.dob),
        }

        lecturer_serializer = LecturerSerializer(instance, data=lecturer_data, partial=True)
        if lecturer_serializer.is_valid():
            lecturer_serializer.save()
            return Response(lecturer_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(lecturer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        self.perform_destroy(instance)

        # Delete the associated User object
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClassDividedViewSet(viewsets.ModelViewSet):
    queryset = ClassDivided.objects.all()
    serializer_class = ClassDividedSerializer
    permission_classes = (AllowAny,)


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer
    permission_classes = (AllowAny,)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Create the user
        user, created = User.objects.get_or_create(username=username,
                                                   defaults={'email': email, 'password': make_password(password),
                                                             'first_name': first_name, 'last_name': last_name})

        # Add the user to the "student_user" group if needed
        student_group, created = Group.objects.get_or_create(name='student_user')
        user.groups.add(student_group)

        request.data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        user.set_password(password)
        user.save()

        student_data = {
            'student_id': request.data.get('student_id'),
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'dob': request.data.get('dob'),
            'user': user.id,
            'enrolled_classes': request.data.get('enrolled_classes', []),
        }
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student = student_serializer.save()

            enrolled_classes = student_serializer.validated_data.get("enrolled_classes")
            for enrolled_class in enrolled_classes:
                scheduled_college_days = enrolled_class.scheduled_collegeDays.all()
                for college_day in scheduled_college_days:
                    Attendance.objects.create(
                        attendance_student=student,
                        attendance_day=college_day,
                        attendance_class=enrolled_class,
                        is_present=False,
                    )

            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update user information
        user_data = request.data.get('user', {})
        instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        password = user_data.get('password')
        if password:
            instance.user.set_password(password)
        instance.user.save()

        # Update student information
        student_data = {
            'student_id': request.data.get('student_id', instance.student_id),
            'username': request.data.get('username', instance.username),
            'first_name': request.data.get('first_name', instance.first_name),
            'last_name': request.data.get('last_name', instance.last_name),
            'email': request.data.get('email', instance.email),
            'dob': request.data.get('dob', instance.dob),
            'user': instance.user.id,
            'enrolled_classes': request.data.get('enrolled_classes', instance.enrolled_classes),
        }
        student_serializer = StudentSerializer(instance, data=student_data, partial=True)
        if student_serializer.is_valid():
            student = student_serializer.save()

            # Update enrolled classes and attendance
            updated_enrolled_classes = set(
                enrolled_class.id for enrolled_class in student_serializer.validated_data.get("enrolled_classes", []))

            # Remove attendance records for classes no longer in the updated list
            outdated_enrolled_classes = set(
                instance.enrolled_classes.all().values_list('id', flat=True)) - updated_enrolled_classes
            Attendance.objects.filter(attendance_student=student,
                                      attendance_class__in=outdated_enrolled_classes).delete()

            # Create or update attendance records for the updated list of classes
            for enrolled_class in student_serializer.validated_data.get("enrolled_classes", []):
                scheduled_college_days = enrolled_class.scheduled_collegeDays.all()
                for college_day in scheduled_college_days:
                    Attendance.objects.get_or_create(
                        attendance_student=student,
                        attendance_day=college_day,
                        attendance_class=enrolled_class,
                        defaults={'is_present': False},
                    )

            return Response(student_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (AllowAny,)
