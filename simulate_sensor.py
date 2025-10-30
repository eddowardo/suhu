#!/usr/bin/env python3
"""
Script simulasi sensor untuk testing dashboard monitoring suhu
Mengirim data dummy ke API Django setiap 10 detik
"""

import requests
import json
import time
import random
from datetime import datetime

# Konfigurasi
API_URL = "http://10.146.1.170:8000/api/sensor-data/"
ROOM_ID = 1

# Rentang nilai dummy
TEMP_BASE = 25.0
TEMP_VARIATION = 3.0
HUMIDITY_BASE = 60.0
HUMIDITY_VARIATION = 10.0

def send_sensor_data(temperature, humidity):
    """Kirim data sensor ke API"""
    data = {
        "room_id": ROOM_ID,
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1)
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if response.status_code == 201:
            print(f"[{timestamp}] ✓ Data terkirim: Suhu {data['temperature']}°C, Kelembapan {data['humidity']}%")
        else:
            print(f"[{timestamp}] ✗ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[{timestamp}] ✗ Connection error: {e}")

def main():
    print("=== SIMULASI SENSOR SUHU & KELEMBAPAN ===")
    print(f"API URL: {API_URL}")
    print("Mengirim data setiap 10 detik...")
    print("Tekan Ctrl+C untuk berhenti")
    print("-" * 50)

    try:
        while True:
            # Generate nilai random berdasarkan base
            temp = TEMP_BASE + random.uniform(-TEMP_VARIATION, TEMP_VARIATION)
            humidity = HUMIDITY_BASE + random.uniform(-HUMIDITY_VARIATION, HUMIDITY_VARIATION)

            # Pastikan dalam rentang reasonable
            temp = max(15, min(35, temp))
            humidity = max(30, min(90, humidity))

            send_sensor_data(temp, humidity)

            # Tunggu 10 detik
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nSimulasi dihentikan oleh user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
