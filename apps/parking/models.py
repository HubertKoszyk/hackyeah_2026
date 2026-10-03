from django.db import models


class Parking(models.Model):
    camera_link = models.URLField(blank=True)


