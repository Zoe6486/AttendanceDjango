from django.urls import path, include
from rest_framework.routers import DefaultRouter

from attendance.views import index, get_user_id
from attendance.viewsets import  UserViewSet, SemesterViewSet, CourseViewSet, LecturerViewSet

router = DefaultRouter()
router.register("users", UserViewSet, "users")
router.register("semesters", SemesterViewSet, "semesters")
router.register("courses", CourseViewSet, "courses")
router.register("lecturers", LecturerViewSet, "lecturers")

urlpatterns = [
    path('', index, name="Home"),
    path('api/', include(router.urls)),
    path("get_user_id/", get_user_id, name="get_user_id"),
]
