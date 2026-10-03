from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_parkings(request):
    return JsonResponse([
        {
            "id": 1,
            "name": "Parking Centrum",
            "lat": 52.2319,
            "lng": 21.0067,
            "totalSpots": 100,
            "freeSpots": 35,
            "status": "available",
        },
        {
            "id": 2,
            "name": "Parking Dworzec",
            "lat": 52.2288,
            "lng": 21.0032,
            "totalSpots": 80,
            "freeSpots": 4,
            "status": "almost_full",
        },
    ], safe=False)


@require_GET
def get_parkings_by_id(request, id):
    return JsonResponse({
        "id": id,
        "name": f"Parking {id}",
        "lat": 52.23,
        "lng": 21.01,
        "totalSpots": 100,
        "freeSpots": 25,
        "status": "available",
    })
