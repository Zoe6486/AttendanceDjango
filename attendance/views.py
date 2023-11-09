from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


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