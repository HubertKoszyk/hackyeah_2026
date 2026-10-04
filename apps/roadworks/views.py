from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import RoadRestriction
from .services import find_conflicts, nearby_parkings
import json
import math


def serialize_restriction(road):
    return {
        "id": road.id,
        "title": road.title,
        "king": road.type,
        "kind_label": road.get_type_display(),
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


@csrf_exempt
@require_POST
def create_roadwork(request):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({"errors": {"body": "Niepoprawny JSON"}}, status=400)

    errors = {}

    title = str(data.get("title", "")).strip()
    if not title:
        errors["title"] = "Podaj nazwę blokady"

    road_type = data.get("kind", RoadRestriction.TypeChoices.ROADWORK)
    if road_type not in RoadRestriction.TypeChoices.values:
        errors["kind"] = "Nieznany rodzaj"

    coords = {}
    for key, limit in (("start_lat", 90), ("start_lng", 180), ("end_lat", 90), ("end_lng", 180)):
        try:
            value = float(data.get(key))
            if not math.isfinite(value) or abs(value) > limit:
                raise ValueError
            coords[key] = value
        except (TypeError, ValueError):
            errors[key] = "Niepoprawna współrzędna"

    dates = {}
    for key in ("start_at", "end_at"):
        try:
            parsed = parse_datetime(str(data.get(key, "")))
        except ValueError:
            parsed = None
        if parsed is None:
            errors[key] = "Niepoprawna data"
            continue
        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(parsed)
        dates[key] = parsed

    if not errors and dates["end_at"] <= dates["start_at"]:
        errors["end_at"] = "Koniec musi być później niż początek"

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    restriction = RoadRestriction.objects.create(
        title=title[:200],
        type=road_type,
        organization=str(data.get("organization", "")).strip()[:120],
        description=str(data.get("description", "")).strip(),
        detour=str(data.get("detour", "")).strip()[:300],
        **coords,
        **dates,
    )
    return JsonResponse(serialize_restriction(restriction), status=201)