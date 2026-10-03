from django.core.management.base import BaseCommand
from apps.parking.models import Parking
from apps.parking.service.parking_service import ParkingService
from apps.parking.repository.camera_repository import CameraRepository
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Parking worker started.")

        service = ParkingService()
        camera_repository = CameraRepository()

        while True:
            parkings = Parking.objects.prefetch_related("cameras")

            for parking in parkings:
                cars_sum = 0

                for camera in parking.cameras.all():
                    photo = camera_repository.get_photo(camera.url)

                    if photo is None:
                        print(f"   brak zdjęcia z kamery {camera.id}, pomijam")
                        continue

                    cars_sum += service.count_vehicles(photo)

                parking.empty_slots = parking.max_slots - cars_sum
                parking.save(update_fields=["empty_slots"])

                print(f"{parking.name}: {parking.empty_slots}")

            print("--- Update finished ---")
            time.sleep(20)