from django.urls import path

from attendance.views import index

urlpatterns = [
    path('', index, name="Home")]
