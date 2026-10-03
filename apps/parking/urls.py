from django.urls import path
from . import views

app_name = "parking"

urlpatterns = [
    path('/get/all', views.get_parkings, name="get_parkings")
]