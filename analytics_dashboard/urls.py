from django.urls import path
from analytics_dashboard import views

urlpatterns = [
    path('',views.analytics_dashboard,name='analytics_dashboard'),
    path('device-diagnostics/',views.device_diagnostics,name='device_diagnostics'),
]