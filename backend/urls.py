from django.contrib import admin
from django.urls import path, include
from users.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', login_view, name='root_login'),
    path('', include(('monitor_suhu.urls', 'monitor_suhu'), namespace='monitor_suhu')),
]
