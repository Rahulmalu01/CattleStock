from django.urls import path
from . import views

urlpatterns = [
    path('sensor-data/',views.sensor_data_api,name='sensor_data_api'),
    path('alerts/',views.alert_api,name='alert_api'),
    path('latest-readings/',views.latest_sensor_data,name='latest_sensor_data'),
    path('latest-alerts/',views.latest_alerts,name='latest_alerts'),
]