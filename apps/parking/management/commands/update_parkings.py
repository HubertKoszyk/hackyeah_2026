```python
from django.core.management.base import BaseCommand
from apps.parking.models import Parking
from apps.parking.service.parking_service import ParkingService
from apps.parking.repository.camera_repository import CameraRepository
import time


class Command(BaseCommand):
    """
    Django management command that periodically updates parking occupancy.

    The command retrieves photos from all cameras assigned to each parking,
    counts the detected vehicles, and updates the number of available
    parking slots in the database.
    """

    def handle(self, *args, **options):
        """
        Continuously update the number of available parking slots.

        For each parking, photos are retrieved from all assigned cameras.
        Vehicles detected in the photos are summed and subtracted from the
        parking's maximum capacity. The resulting number of available slots
        is saved to the database.

        The process repeats every 20 seconds.
        """
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
                        print(f"   No photo from camera {camera.id}, skipping")
                        continue

                    cars_sum += service.count_vehicles(photo)

                parking.empty_slots = parking.max_slots - cars_sum
                parking.save(update_fields=["empty_slots"])

                print(f"{parking.name}: {parking.empty_slots} available slots")

            print("--- Update finished ---")
            time.sleep(20)
```
