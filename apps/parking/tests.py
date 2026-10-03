from django.test import TestCase
from django.urls import reverse

from .models import Parking, Camera

class ParkingTestCase(TestCase):
    # get/all
    def test_get_parkings_empty_database(self):
        response = self.client.get(
            reverse("parking:get_parkings")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_parkings(self):
        parking = Parking.objects.create(
            adres="123 Test Street",
            gps_code="52.2319,21.0067",
            name="Test Parking",
            max_slots=100,
            empty_slots=50,
        )

        response = self.client.get(
            reverse("parking:get_parkings")
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            [
                {
                    "id": parking.id,
                    "name": "Test Parking",
                    "adres": "123 Test Street",
                    "gps_code": "52.2319,21.0067",
                    "cameras": {},
                    "lat": 52.2319,
                    "lng": 21.0067,
                    "totalSpots": 100,
                    "freeSpots": 50,
                    "occupancy_percent": 50.0,
                    "status": "Low",
                }
            ],
        )

    def test_get_parkings_with_cameras(self):
        parking = Parking.objects.create(
            adres="123 Test Street",
            gps_code="52.2319,21.0067",
            name="Test Parking",
            max_slots=100,
            empty_slots=25,
        )

        Camera.objects.create(
            parking=parking,
            url="https://example.com/camera1",
        )

        Camera.objects.create(
            parking=parking,
            url="https://example.com/camera2",
        )

        response = self.client.get(
            reverse("parking:get_parkings")
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["cameras"],
            {
                "camera1": "https://example.com/camera1",
                "camera2": "https://example.com/camera2",
            },
        )

    # get/<int:id>/
    def test_get_parking_by_id(self):
        parking = Parking.objects.create(
            adres="123 Test Street",
            gps_code="52.2319,21.0067",
            name="Test Parking",
            max_slots=100,
            empty_slots=50,
        )

        response = self.client.get(
            reverse(
                "parking:get_parkings_by_id",
                args=[parking.id],
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            {
                "id": parking.id,
                "name": "Test Parking",
                "adres": "123 Test Street",
                "gps_code": "52.2319,21.0067",
                "cameras": {},
                "lat": 52.2319,
                "lng": 21.0067,
                "totalSpots": 100,
                "freeSpots": 50,
                "occupancy_percent": 50.0,
                "status": "Low",
            },
        )

    def test_get_parking_by_id_not_found(self):
        response = self.client.get(
            reverse(
                "parking:get_parkings_by_id",
                args=[999999],
            )
        )

        self.assertEqual(response.status_code, 404)