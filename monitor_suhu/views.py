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

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('/users/login/')

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
    Returns None if insufficient data.
    """
    from django.utils import timezone
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)

    # Get data from last 10 minutes
    recent_readings = TemperatureReading.objects.filter(
        timestamp__gte=ten_minutes_ago
    ).order_by('timestamp')

    if len(recent_readings) < 2:
        # If not enough data, return None
        return None

    # Prepare data for linear regression
    timestamps = [(r.timestamp - ten_minutes_ago).total_seconds() / 60 for r in recent_readings]  # minutes from start
    temperatures = [r.temperature for r in recent_readings]
    humidities = [r.humidity for r in recent_readings if r.humidity is not None]

    # Predict temperature
    temp_model = LinearRegression()
    temp_model.fit(np.array(timestamps).reshape(-1, 1), temperatures)
    future_minutes = 10 + (hours * 60)  # 10 minutes from now + 2 hours
    predicted_temp = temp_model.predict(np.array([future_minutes]).reshape(-1, 1))[0]

    # Predict humidity if enough data
    if len(humidities) >= 2:
        hum_timestamps = [(r.timestamp - ten_minutes_ago).total_seconds() / 60 for r in recent_readings if r.humidity is not None]
        hum_model = LinearRegression()
        hum_model.fit(np.array(hum_timestamps).reshape(-1, 1), humidities)
        predicted_hum = hum_model.predict(np.array([future_minutes]).reshape(-1, 1))[0]
    else:
        # Use average humidity if not enough data
        predicted_hum = sum(h.humidity for h in recent_readings if h.humidity) / len([h for h in recent_readings if h.humidity]) if any(h.humidity for h in recent_readings) else 60

    return {'suhu_prediksi': round(predicted_temp, 1), 'kelembapan_prediksi': round(predicted_hum, 1)}

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
            "humidity": latest_reading.humidity,
            "timestamp": latest_reading.timestamp
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        # Jika tidak ada data, kembalikan error
        return Response({
            "error": "No sensor data available",
            "message": "Belum ada data sensor yang diterima"
        }, status=status.HTTP_404_NOT_FOUND)

# ===== API untuk menerima data sensor dari NodeMCU =====
@api_view(['POST'])
def receive_sensor_data(request):
    """
    Menerima data sensor dari NodeMCU dan menyimpannya ke database.
    """
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        # Simpan data suhu dan kelembapan
        temperature = serializer.validated_data.get('temperature')
        humidity = serializer.validated_data.get('humidity')

        # Buat objek TemperatureReading baru
        reading = TemperatureReading.objects.create(
            temperature=temperature,
            humidity=humidity
        )

        return Response({
            "message": "Data sensor berhasil diterima",
            "id": reading.id,
            "temperature": temperature,
            "humidity": humidity
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ===== API untuk mendapatkan status kenyamanan =====
@api_view(['GET'])
def get_comfort_status(request):
    """
    Mengembalikan status kenyamanan berdasarkan data sensor terbaru.
    """
    latest_reading = TemperatureReading.objects.order_by('-timestamp').first()
    if latest_reading:
        comfort_status = predict_comfort(latest_reading.temperature, latest_reading.humidity)
        return Response({"comfort_status": comfort_status}, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": "No sensor data available",
            "message": "Belum ada data sensor untuk menentukan status kenyamanan"
        }, status=status.HTTP_404_NOT_FOUND)

# ===== HTML View =====
@login_required
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
        comfort_status = predict_comfort(latest_reading.temperature, latest_reading.humidity)
        kelembapan_saat_ini = latest_reading.humidity

        # Prediksi suhu dan kelembapan 2 jam kedepan
        predictions = predict_future_temp_humidity(hours=2)

        context = {
            'sensor_data': sensor_data,
            'latest_temperature': latest_reading.temperature,
            'latest_humidity': latest_reading.humidity,
            'comfort_status': comfort_status,
            'kelembapan_saat_ini': kelembapan_saat_ini,
            'suhu_prediksi_2jam': predictions['suhu_prediksi'] if predictions else None,
            'kelembapan_prediksi_2jam': predictions['kelembapan_prediksi'] if predictions else None,
            'today_date': datetime.now().strftime('%d %B %Y'),
        }
    else:
        # Jika belum ada data
        context = {
            'sensor_data': [],
            'latest_temperature': None,
            'latest_humidity': None,
            'comfort_status': 'Belum ada data sensor',
            'kelembapan_saat_ini': None,
            'suhu_prediksi_2jam': None,
            'kelembapan_prediksi_2jam': None,
            'today_date': datetime.now().strftime('%d %B %Y'),
        }

    return render(request, 'monitor_suhu/index.html', context)
