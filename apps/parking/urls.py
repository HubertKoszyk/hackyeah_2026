from django.urls import path
from . import views

app_name = "parking"

urlpatterns = [
    path('get/all/', views.get_parkings, name="get_parkings"),
    path('get/<int:id>/', views.get_parkings_by_id, name="get_parkings_by_id"),
    path('get_slots_data/<int:id>', views.get_slots_data, name="get_slots_data"),
    path('test_image', views.test_image, name="test_image"),
]