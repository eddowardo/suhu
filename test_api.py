#!/usr/bin/env python3
"""
Script untuk test API endpoint secara real-time
"""

import requests
import time

def test_api():
    print('Testing API endpoint setiap 5 detik selama 30 detik...')

    for i in range(6):
        try:
            response = requests.get('http://10.146.1.170:8000/api/latest-sensor-data/')
            data = response.json()
            print(f'[{i+1}] Status: {response.status_code}, Suhu: {data["temperature"]}°C, Kelembapan: {data["humidity"]}%')
        except Exception as e:
            print(f'[{i+1}] Error: {e}')

        if i < 5:
            time.sleep(5)

    print('Testing selesai.')

if __name__ == "__main__":
    test_api()
