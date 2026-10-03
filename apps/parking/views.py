from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from .repository.camera_repository import CameraRepository


from .models import Parking


def get_occupancy_percent(taken_slots, max_slots):
    empty_slots = max_slots - taken_slots
    occupancy_percent = (max_slots / taken_slots) * 100

    return occupancy_percent


def get_parking_status(occupancy_percent):
    status = "Unknown" 

    if occupancy_percent <= 20:
        status = "Empty"
    elif occupancy_percent <= 50:
        status = "Low"
    elif occupancy_percent <= 75:
        status = "Medium"
    elif occupancy_percent <= 95:
        status = "High"
    elif occupancy_percent > 95:
        status = "Full"

    return status


def serialize_parking(parking):
    cameras = {}
    all_cameras = parking.cameras.all()

    camera_num = 1

    for camera in all_cameras:
        name = "camera" + str(camera_num)
        cameras[name] = camera.url
        camera_num += 1

    occupancy_percent = get_occupancy_percent(50, 100)
    parking_status = get_parking_status(occupancy_percent)

    return {
        "id": parking.id,
        "name": parking.name,
        "adres": parking.adres,
        "gps_code": parking.gps_code,
        "cameras": cameras,
        "lat": 52.2319,
        "lng": 21.0067,
        "totalSpots": 100,
        "freeSpots": 35,
        'occupancy_percent': occupancy_percent,
        "status": parking_status,
    }


@require_GET
def get_parkings(request):
    parkings = Parking.objects.prefetch_related("cameras")
    data = []

    for parking in parkings:
        data.append(serialize_parking(parking))

    return JsonResponse(data, safe=False)


@require_GET
def get_parkings_by_id(request, id):
    parking = get_object_or_404(Parking.objects.prefetch_related("cameras"), id=id)
    return JsonResponse(serialize_parking(parking))


@require_GET
def get_slots_data(request, id):
    parking = get_object_or_404(Parking.objects.prefetch_related("cameras"), id=id)
    occupancy_percent = get_occupancy_percent(1, 100)
    parking_status = get_parking_status(occupancy_percent)

    return {
        "totalSpots": 100,
        "freeSpots": 35,
        "occupancyPercent": occupancy_percent,
        "status": parking_status,
    }


def test_image(request):
    photo = CameraRepository().get_photo("https://www.worldcam.pl/liveview/36999")
    if photo is None:
        return HttpResponse("nie udalo sie pobrac zdjecia", status=500)
    return HttpResponse(f"ok, rozmiar zdjecia: {photo.shape}")