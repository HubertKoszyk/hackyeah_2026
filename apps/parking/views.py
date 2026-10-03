from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET


from .models import Parking


def serialize_parking(parking):
    cameras = {}
    all_cameras = parking.cameras.all()

    camera_num = 1

    for camera in all_cameras:
        name = "camera" + str(camera_num)
        cameras[name] = camera.url
        camera_num += 1

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
        "status": "available",
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

