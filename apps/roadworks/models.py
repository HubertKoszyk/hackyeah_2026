from django.db import models
from django.utils import timezone


class RoadRestriction(models.Model):
    class TypeChoices(models.TextChoices):
        ROADWORK = "roadwork", "Roboty drogowe"
        EVENT = "event", "Wydarzenie"
        ACCIDENT = "accident", "Wypadek / awaria"
        CLOSURE = "closure", "Zamknięcie drogi"

    title = models.CharField("Nazwa", max_length=200)
    type = models.CharField("Rodzaj", max_length=20, choices=TypeChoices.choices, default=TypeChoices.ROADWORK)
    organization = models.CharField("Zgłaszający", max_length=120, blank=True, 
                                    help_text="np. ZIKiT, Wodociągi, Energetyka")
    description = models.TextField("Opis", blank=True)
    detour = models.CharField("Objazd", max_length=300, blank=True)

    start_lat = models.FloatField("Początek - szer. geogr.")
    start_lng = models.FloatField("Początek - dł. geogr.")
    end_lat = models.FloatField("Koniec - szer. geogr.")
    end_lng = models.FloatField("Koniec - dł. geogr.")

    start_at = models.DateTimeField("Od")
    end_at = models.DateTimeField("Do")

    class Meta:
        ordering = ["start_at"]
        verbose_name = "Ograniczenie drogowe"
        verbose_name_plural = "Ograniczenia drogowe"

    def __str__(self):
        return self.title

    @property
    def status(self):
        now = timezone.now()
        if self.end_at < now:
            return "finished"
        if self.start_at > now:
            return "planned"
        return "active"
