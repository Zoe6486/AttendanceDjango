from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_user_id(request):
    user = request.user
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)


class logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

