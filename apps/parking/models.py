from django.db import models


class Parking(models.Model):
    adres = models.CharField(max_length=250)
    gps_code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    max_slots = models.PositiveBigIntegerField(blank=True, default=100)
    empty_slots = models.PositiveBigIntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class Camera(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name="cameras")
    url = models.URLField(blank=True)

    def __str__(self):
        return f"Camera {self.id} - {self.parking.name}"
