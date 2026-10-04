from django.urls import path
from . import views

app_name = "roadworks"

urlpatterns = [
    path("", views.get_roadworks, name="get_roadworks"),
]