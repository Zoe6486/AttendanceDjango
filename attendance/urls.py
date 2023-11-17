from django.urls import path, include
from rest_framework.routers import DefaultRouter

from attendance.views import index
from attendance.viewsets import SemesterViewSet, CourseViewSet

router = DefaultRouter()
router.register("semesters", SemesterViewSet, "semesters")
router.register("courses", CourseViewSet, "courses")

urlpatterns = [
    path('', index, name="Home"),
    path('api/', include(router.urls)),
]
