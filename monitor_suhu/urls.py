app_name = 'monitor_suhu'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # halaman utama HTML
    path('api/rooms/', views.RoomList.as_view(), name='api_rooms'),
    path('api/readings/', views.TemperatureList.as_view(), name='api_readings'),
    path('api/sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),  # Endpoint untuk sensor
    path('api/comfort-status/', views.get_comfort_status, name='get_comfort_status'),  # Endpoint untuk status kenyamanan
    path('api/latest-sensor-data/', views.get_latest_sensor_data, name='get_latest_sensor_data'),  # Endpoint untuk data sensor terbaru
]
