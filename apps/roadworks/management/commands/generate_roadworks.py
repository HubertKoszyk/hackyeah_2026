from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.roadworks.models import RoadRestriction


class Command(BaseCommand):
    help = "Dodaje przykładowe (fikcyjne) ograniczenia drogowe do demo"

    def handle(self, *args, **options):
        now = timezone.now()
        RoadRestriction.objects.all().delete()
        data = [
            dict(title="Remont nawierzchni - ul. Długa", type="roadwork", organization="ZIKiT",
                 description="Frezowanie i nowa warstwa ścieralna.", detour="Objazd ul. Basztową",
                 start_lat=50.0685, start_lng=19.9383, end_lat=50.0660, end_lng=19.9385,
                 start_at=now - timedelta(days=1), end_at=now + timedelta(days=9)),
            dict(title="Wymiana sieci wodociągowej - ul. Długa", type="roadwork",
                 organization="Wodociągi", description="Wykop poprzeczny.",
                 start_lat=50.0670, start_lng=19.9384, end_lat=50.0663, end_lng=19.9385,
                 start_at=now + timedelta(days=5), end_at=now + timedelta(days=12)),
            dict(title="Mecz - zamknięcie al. Reymonta", type="event", organization="Biuro Zarządzania Ruchem",
                 description="Zamknięcie na czas imprezy masowej.", detour="Objazd ul. Piastowską",
                 start_lat=50.0630, start_lng=19.9220, end_lat=50.0645, end_lng=19.9100,
                 start_at=now + timedelta(days=2), end_at=now + timedelta(days=2, hours=6)),
            dict(title="Wypadek - al. 29 Listopada", type="accident", organization="Policja / ZDMK",
                 description="Zablokowany prawy pas.", detour="Objazd ul. Opolską",
                 start_lat=50.0870, start_lng=19.9560, end_lat=50.0880, end_lng=19.9620,
                 start_at=now - timedelta(hours=1), end_at=now + timedelta(hours=3)),
        ]
        for item in data:
            RoadRestriction.objects.create(**item)
        print(f"Dodano {len(data)} ograniczeń (dane przykładowe)")