from django.urls import path
from . import views

app_name = "roadworks"

urlpatterns = [
    path("", views.get_roadworks, name="get_roadworks"),
    path("create/", views.create_roadwork, name="create_roadwork"),
    path("<int:id>/delete/", views.delete_roadwork, name="delete_roadwork"),
]