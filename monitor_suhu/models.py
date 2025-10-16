from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class TemperatureReading(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='readings')
    temperature = models.FloatField()
    humidity = models.FloatField(null=True, blank=True)  # Tambah field humidity
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.room.name} - {self.temperature}°C, {self.humidity}% at {self.timestamp:%Y-%m-%d %H:%M}"
