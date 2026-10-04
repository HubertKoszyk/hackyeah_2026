from math import asin, cos, radians, sin, sqrt

from apps.parking.models import Parking

from .models import RoadRestriction

CONFLICT_DISTANCE_M = 150
PARKING_RADIUS_M = 500


def haversine_m(lat1, lng1, lat2, lng2):
    # distance between two gps points
    r = 6371000
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return 2 * r * asin(sqrt(a))


def _points(restriction):
    # begining, middle, end of an road segment
    mid_lat = (restriction.start_lat + restriction.end_lat) / 2
    mid_lng = (restriction.start_lng + restriction.end_lng) / 2
    return [
        (restriction.start_lat, restriction.start_lng),
        (mid_lat, mid_lng),
        (restriction.end_lat, restriction.end_lng),
    ]


def segment_distance_m(a, b):
    # Approximate distance between two road segments
    # The minimum distance between any points on them
    return min(
        haversine_m(p[0], p[1], q[0], q[1])
        for p in _points(a)
        for q in _points(b)
    )


def find_conflicts(restriction):
    # Other circumstances nearby this road segment
    """Inne ograniczenia, które nakładają się czasowo i leżą blisko tego odcinka."""
    candidates = RoadRestriction.objects.filter(
        start_at__lte=restriction.end_at,
        end_at__gte=restriction.start_at,
    )
    if restriction.pk:
        candidates = candidates.exclude(pk=restriction.pk)
    return [c for c in candidates if segment_distance_m(restriction, c) <= CONFLICT_DISTANCE_M]


def parse_gps(value):
    # '50.0617, 19.9373' -> (50.0617, 19.9373)
    # Returns None if bad format
    try:
        lat, lng = [float(x) for x in value.replace(";", ",").split(",")]
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return lat, lng
    except (ValueError, AttributeError):
        pass
    return None


def nearby_parkings(restriction):
    # Returns Paringis in PARKING_RADIUS_M distance from middle segment
    _, mid, _ = _points(restriction)
    result = []
    for parking in Parking.objects.all():
        coords = parse_gps(parking.gps_code)
        if coords is None:
            continue
        distance = haversine_m(mid[0], mid[1], coords[0], coords[1])
        if distance <= PARKING_RADIUS_M:
            result.append({"id": parking.id, "name": parking.name, "distance_m": round(distance)})
    return sorted(result, key=lambda p: p["distance_m"])