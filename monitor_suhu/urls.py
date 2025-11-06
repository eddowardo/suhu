app_name = 'monitor_suhu'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # halaman utama - redirect ke login jika belum login
    path('dashboard/', views.index, name='index'),  # halaman dashboard
    path('api/sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),  # Endpoint untuk sensor
    path('api/comfort-status/', views.get_comfort_status, name='get_comfort_status'),  # Endpoint untuk status kenyamanan
    path('api/latest-sensor-data/', views.get_latest_sensor_data, name='get_latest_sensor_data'),  # Endpoint untuk data sensor terbaru
]
