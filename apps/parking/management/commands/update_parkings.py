from django.core.management.base import BaseCommand
from apps.parking.models import Parking
import random
import time


class Command(BaseCommand):
    help = "Testowo aktualizuje liczbę wolnych miejsc na parkingach"

    def handle(self, *args, **options):
        print("Parking worker started.")
        while True:
            parkings = Parking.objects.all()

            for parking in parkings:
                parking.empty_slots = random.randint(0, 100)
                parking.save(update_fields=["empty_slots"])

                print(f"{parking.name}: {parking.empty_slots} wolnych miejsc")

            print("--- Update finished ---")

            time.sleep(20)