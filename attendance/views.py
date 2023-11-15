from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from attendance.models import Semester
from attendance.serializers import SemesterSerializer


# Create your views here.
@api_view(["GET"])
def index(request):
    return Response(
        {
            "data": [
                {"name": "Lei Song",
                 "address": "123 Carrington Road",
                 "phone": "1233242"
                 },
                {"name": "Chris",
                 "address": "123 Carrington Road",
                 "phone": "1233242"
                 },
            ]
        }
    )


@api_view(["GET"])
def semester_list(request):
    if request.method == "GET":
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
