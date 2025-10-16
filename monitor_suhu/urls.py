app_name = 'monitor_suhu'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # halaman utama HTML
    path('api/rooms/', views.RoomList.as_view(), name='api_rooms'),
    path('api/readings/', views.TemperatureList.as_view(), name='api_readings'),
    path('api/sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),  # Endpoint untuk sensor
]
