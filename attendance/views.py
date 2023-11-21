from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Semester, Lecturer
from attendance.serializers import SemesterSerializer, LecturerSerializer, UserSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    return Response(
        {
            "data": [
                {"name": "Chris",
                 "address": "123 Carrington Road",
                 "phone": "1233242"
                 },
            ]
        }
    )


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_user_id(request):
    user = request.user
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)


class logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# @api_view(["GET"])
# def semester_list(request):
#     if request.method == "GET":
#         semesters = Semester.objects.all()
#         serializer = SemesterSerializer(semesters, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = SemesterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
class LecturerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

    def perform_create(self, serializer):
        # Logic for creating a new Lecturer instance
        user_data = serializer.validated_data.pop('user', {})
        user = User.objects.create_user(**user_data)
        lecturer = serializer.save(user=user)


class LecturerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer

    def perform_update(self, serializer):
        # Logic for updating an existing Lecturer instance
        lecturer = serializer.save()

        # Update related User instance
        user = lecturer.user
        user.username = serializer.validated_data.get('username', user.username)
        user.email = serializer.validated_data.get('email', user.email)
        user.first_name = serializer.validated_data.get('first_name', user.first_name)
        user.last_name = serializer.validated_data.get('last_name', user.last_name)
        user.save()

    def perform_destroy(self, instance):
        # Logic for deleting a Lecturer instance
        user = instance.user
        user.delete()
        instance.delete()
