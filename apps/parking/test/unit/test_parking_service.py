import unittest
import cv2
import numpy as np
from service.parking_service import ParkingService
from pathlib import Path

RESOURCE_DIR = Path(__file__).resolve().parents[1] / "resources"

class TestParkingService(unittest.TestCase):
    def setUp(self):
        self.parking_service = ParkingService()

    def test_count_vehicles(self):
        image = cv2.imread(str(RESOURCE_DIR / "3cars.png"))
        self.assertEqual(self.parking_service.count_vehicles(image), 3)

        image = cv2.imread(str(RESOURCE_DIR / "4cars.png"))
        self.assertEqual(self.parking_service.count_vehicles(image), 4)

        image = cv2.imread(str(RESOURCE_DIR / "2cars.png"))
        self.assertEqual(self.parking_service.count_vehicles(image), 2)

        image = cv2.imread(str(RESOURCE_DIR / "1cars.png"))
        self.assertEqual(self.parking_service.count_vehicles(image), 1)

        image = cv2.imread(str(RESOURCE_DIR / "0cars.png"))
        self.assertEqual(self.parking_service.count_vehicles(image), 0)
