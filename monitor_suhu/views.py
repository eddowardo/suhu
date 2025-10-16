from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room, TemperatureReading
from .serializers import RoomSerializer, TemperatureReadingSerializer, SensorDataSerializer
from datetime import datetime

# ===== API Views =====
class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TemperatureList(generics.ListCreateAPIView):
    queryset = TemperatureReading.objects.all()
    serializer_class = TemperatureReadingSerializer

# ===== Home View =====
def home(request):
    if request.user.is_authenticated:
        return redirect('monitor_suhu:index')
    return render(request, 'monitor_suhu/home.html')

# ===== API untuk menerima data dari sensor =====
@api_view(['POST'])
def receive_sensor_data(request):
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        room_id = serializer.validated_data['room_id']
        temperature = serializer.validated_data['temperature']
        humidity = serializer.validated_data.get('humidity')

        try:
            room = Room.objects.get(id=room_id)
            TemperatureReading.objects.create(
                room=room,
                temperature=temperature,
                humidity=humidity
            )
            return Response({"message": "Data received successfully"}, status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ===== HTML View =====
@login_required
def index(request):
    rooms = Room.objects.all().prefetch_related('readings')
    # Ambil data terbaru dari database untuk sensor aktif
    sensor_aktif = []
    for room in rooms:
        latest_reading = room.readings.order_by('-timestamp').first()
        if latest_reading:
            sensor_aktif.append({
                'nama': f'Sensor {room.name}',
                'value': latest_reading.temperature
            })

    # Jika tidak ada data, gunakan dummy
    if not sensor_aktif:
        sensor_aktif = [
            {'nama': 'Sensor Ruang Tamu', 'value': 24},
            {'nama': 'Sensor Kamar', 'value': 23},
            {'nama': 'Sensor Dapur', 'value': 25},
            {'nama': 'Sensor Gudang', 'value': 22},
        ]

    # Hitung suhu prediksi dari rata-rata readings terbaru
    recent_readings = TemperatureReading.objects.filter(timestamp__date=datetime.now().date())[:10]
    if recent_readings:
        avg_temp = sum(r.temperature for r in recent_readings) / len(recent_readings)
        suhu_prediksi = round(avg_temp, 1)
    else:
        suhu_prediksi = 24

    context = {
        'rooms': rooms,
        'today_date': datetime.now().strftime('%d %B %Y'),
        'suhu_prediksi': suhu_prediksi,
        'perubahan_suhu': 1.2,  # Tetap dummy untuk sekarang
        'perubahan_persen': 5.42,
        'estimasi_penggunaan': len(sensor_aktif),
        'sensor_aktif': sensor_aktif,
        'intensitas_suhu': 47,
        'emisi': 36.4,
        'energi_hijau': 100,
        'suhu_kemarin': 23,
    }
    return render(request, 'monitor_suhu/index.html', context)
