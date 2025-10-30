#!/usr/bin/env python
"""
Script untuk monitoring data sensor secara real-time
"""
import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from monitor_suhu.models import TemperatureReading

def monitor_sensor_data():
    """Monitor data sensor secara real-time"""
    print('Monitoring sensor data secara real-time...')
    print('Tekan Ctrl+C untuk berhenti')
    print('=' * 50)

    last_count = 0
    while True:
        try:
            count = TemperatureReading.objects.count()
            if count > last_count:
                latest = TemperatureReading.objects.order_by('-timestamp').first()
                timestamp_str = latest.timestamp.strftime('%H:%M:%S')
                print(f'[{timestamp_str}] Suhu: {latest.temperature}°C, Kelembapan: {latest.humidity}%')
                last_count = count
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nMonitoring dihentikan.')
            break
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(1)

if __name__ == '__main__':
    monitor_sensor_data()
