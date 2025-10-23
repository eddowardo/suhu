from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),  # Disabled temporarily
    path('', include(('monitor_suhu.urls', 'monitor_suhu'), namespace='monitor_suhu')),
]
