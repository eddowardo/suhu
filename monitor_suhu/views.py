from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room, TemperatureReading
from .serializers import RoomSerializer, TemperatureReadingSerializer, SensorDataSerializer
from datetime import datetime, timedelta
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load AI model for thermal comfort
MODEL_PATH = '../Downloads/thermal_comfort_rf_model.pkl'
try:
    comfort_model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    comfort_model = None

def predict_comfort(ta, rh):
    """
    Predict thermal comfort status using AI model.
    Simplified to only use temperature and humidity.
    Returns: 'Nyaman', 'Tidak Nyaman Panas', 'Tidak Nyaman Dingin'
    """
    if comfort_model is None:
        return 'Model tidak tersedia'

    # Simple rule-based prediction since the model expects different features
    if ta >= 24 and ta <= 27 and rh >= 40 and rh <= 70:
        return 'Nyaman'
    elif ta > 27:
        return 'Tidak Nyaman Panas'
    elif ta < 24:
        return 'Tidak Nyaman Dingin'
    else:
        return 'Nyaman'  # Default to comfortable if borderline

def predict_future_temp_humidity(hours=2):
    """
    Predict temperature and humidity 2 hours ahead using historical data trend.
    Uses data from last 10 minutes to calculate simple linear trend.
    """
    from django.utils import timezone
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)

    # Get data from last 10 minutes
    recent_readings = TemperatureReading.objects.filter(
        timestamp__gte=ten_minutes_ago
    ).order_by('timestamp')

    if len(recent_readings) < 2:
        # If not enough data, return average or default
        all_recent = TemperatureReading.objects.filter(
            timestamp__date=now.date()
        )[:10]
        if all_recent:
            avg_temp = sum(r.temperature for r in all_recent) / len(all_recent)
            avg_hum = sum(r.humidity for r in all_recent if r.humidity) / len([r for r in all_recent if r.humidity]) if any(r.humidity for r in all_recent) else 60
        else:
            avg_temp = 25
            avg_hum = 60
        return {'suhu_prediksi': round(avg_temp, 1), 'kelembapan_prediksi': round(avg_hum, 1)}

    # Calculate time differences and values
    timestamps = [(r.timestamp - ten_minutes_ago).total_seconds() / 3600 for r in recent_readings]  # hours from start
    temps = [r.temperature for r in recent_readings]
    hums = [r.humidity if r.humidity else 60 for r in recent_readings]  # default humidity if None

    # Simple linear regression for trend
    temp_model = LinearRegression()
    temp_model.fit(np.array(timestamps).reshape(-1, 1), temps)
    future_time = (now - ten_minutes_ago).total_seconds() / 3600 + hours
    predicted_temp = temp_model.predict([[future_time]])[0]

    hum_model = LinearRegression()
    hum_model.fit(np.array(timestamps).reshape(-1, 1), hums)
    predicted_hum = hum_model.predict([[future_time]])[0]

    return {
        'suhu_prediksi': round(max(15, min(40, predicted_temp)), 1),  # clamp to reasonable range
        'kelembapan_prediksi': round(max(20, min(100, predicted_hum)), 1)
    }

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

# ===== API untuk mendapatkan status kenyamanan =====
@api_view(['GET'])
def get_comfort_status(request):
    """
    Mengembalikan status kenyamanan berdasarkan data sensor terbaru.
    Output: salah satu dari 'Nyaman', 'Tidak Nyaman Panas', 'Tidak Nyaman Dingin'
    """
    latest_reading = TemperatureReading.objects.order_by('-timestamp').first()
    if latest_reading:
        comfort_status = predict_comfort(latest_reading.temperature, latest_reading.humidity or 60)
    else:
        # Jika tidak ada data, gunakan nilai default
        comfort_status = predict_comfort(25, 60)  # Suhu default 25°C, kelembapan 60%

    return Response({"comfort_status": comfort_status}, status=status.HTTP_200_OK)

# ===== API untuk mendapatkan data sensor terbaru =====
@api_view(['GET'])
def get_latest_sensor_data(request):
    """
    Mengembalikan data sensor terbaru (suhu dan kelembapan).
    """
    latest_reading = TemperatureReading.objects.order_by('-timestamp').first()
    if latest_reading:
        data = {
            "temperature": latest_reading.temperature,
            "humidity": latest_reading.humidity or 60,
            "timestamp": latest_reading.timestamp
        }
    else:
        # Jika tidak ada data, gunakan nilai default
        data = {
            "temperature": 25.0,
            "humidity": 60.0,
            "timestamp": None
        }

    return Response(data, status=status.HTTP_200_OK)

# ===== HTML View =====
# @login_required  # Disabled temporarily
def index(request):
    # Ambil 10 data sensor terbaru untuk ditampilkan
    recent_readings = TemperatureReading.objects.all().order_by('-timestamp')[:10]

    # Jika ada data, tampilkan dalam format terminal-like
    if recent_readings:
        sensor_data = []
        for reading in recent_readings:
            sensor_data.append({
                'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': reading.temperature,
                'humidity': reading.humidity
            })

        # Data terbaru untuk dashboard
        latest_reading = recent_readings[0]
        comfort_status = predict_comfort(latest_reading.temperature, latest_reading.humidity or 60)
        kelembapan_saat_ini = latest_reading.humidity or 60

        context = {
            'sensor_data': sensor_data,
            'latest_temperature': latest_reading.temperature,
            'latest_humidity': latest_reading.humidity,
            'comfort_status': comfort_status,
            'kelembapan_saat_ini': kelembapan_saat_ini,
            'today_date': datetime.now().strftime('%d %B %Y'),
        }
    else:
        # Jika belum ada data
        context = {
            'sensor_data': [],
            'latest_temperature': None,
            'latest_humidity': None,
            'comfort_status': 'Menunggu data sensor...',
            'kelembapan_saat_ini': 60,
            'today_date': datetime.now().strftime('%d %B %Y'),
        }

    return render(request, 'monitor_suhu/index.html', context)
