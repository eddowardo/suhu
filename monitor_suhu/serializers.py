from rest_framework import serializers
from .models import Room, TemperatureReading

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TemperatureReadingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = TemperatureReading
        fields = '__all__'

# Serializer untuk input data dari sensor (POST)
class SensorDataSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField(required=False)  # Optional untuk backward compatibility
