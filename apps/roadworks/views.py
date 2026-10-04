from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import RoadRestriction
from .services import find_conflicts, nearby_parkings


def serialize_restriction(road):
    return {
        "id": road.id,
        "title": road.title,
        "type": road.type,
        "type_label": road.get_type_display(),
        "organization": road.organization,
        "description": road.description,
        "detour": road.detour,
        "status": road.status,
        "start": {"lat": road.start_lat, "lng": road.start_lng},
        "end": {"lat": road.end_lat, "lng": road.end_lng},
        "start_at": road.start_at.isoformat(),
        "end_at": road.end_at.isoformat(),
        "conflicts": [{"id": c.id, "title": c.title} for c in find_conflicts(road)],
        "nearby_parkings": nearby_parkings(road),
    }


@require_GET
def get_roadworks(request):
    items = []
    for road in RoadRestriction.objects.all():
        items.append(serialize_restriction(road))

    if request.GET.get("hide_finished") == "1":
        filtered_items = []
        for item in items:
            if item["status"] != "finished":
                filtered_items.append(item)
        items = filtered_items

    return JsonResponse(items, safe=False)
