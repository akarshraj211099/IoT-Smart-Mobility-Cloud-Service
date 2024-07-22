# urls.py (in sensors app)
from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.qr_scan, name='qr_scan'),
    path('sensor/<str:qr_code>/', views.sensor_detail, name='sensor_detail'),
    path('options/', views.options, name='options'),
    path('sensor_id/', views.sensor_id, name='sensor_id'),
]

