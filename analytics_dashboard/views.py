from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hardware.models import (SensorReading, Device)
from cattle_manager.models import CattleProfile
from collections import Counter

def analytics_access(user):
    return user.role in [
        'admin',
        'manager',
        'cattle_manager'
    ]

@login_required
def analytics_dashboard(request):
    if not analytics_access(request.user):
        return render(request, '403.html')
    readings = SensorReading.objects.all().order_by('-timestamp')
    total_cattle = CattleProfile.objects.count()
    total_readings = readings.count()
    devices = Device.objects.all()
    avg_temp = 0
    avg_heart_rate = 0
    avg_milk = 0
    if total_readings > 0:
        avg_temp = round(sum(r.body_temperature for r in readings) / total_readings, 2)
        avg_heart_rate = round(sum(r.heart_rate for r in readings) / total_readings, 2)
        avg_milk = round(sum(r.milk_yield_liters for r in readings) / total_readings, 2)
    activity_data = Counter(
        readings.values_list(
            'activity_level',
            flat=True
        )
    )
    latest_readings = readings[:20]
    temp_labels = [r.timestamp.strftime('%H:%M') for r in latest_readings]
    temp_values = [r.body_temperature for r in latest_readings]
    heart_values = [r.heart_rate for r in latest_readings]
    milk_values = [r.milk_yield_liters for r in latest_readings]
    battery_values = [r.battery_level_percent for r in latest_readings]
    high_temp_count = readings.filter(body_temperature__gt=39.5).count()
    low_activity_count = readings.filter(activity_level='low').count()
    critical_battery_count = readings.filter(battery_level_percent__lt=20).count()
    abnormal_heart_rate = readings.filter(heart_rate__gt=90).count()
    ai_health_score = 100
    ai_health_score -= high_temp_count * 2
    ai_health_score -= low_activity_count * 2
    ai_health_score -= critical_battery_count * 3
    ai_health_score -= abnormal_heart_rate * 2
    if ai_health_score < 0:
        ai_health_score = 0
    online_devices = readings.filter(signal_strength_percent__gte=70).count()
    offline_devices = readings.filter(signal_strength_percent__lt=20).count()
    low_battery_devices = readings.filter(battery_level_percent__lt=20).count()
    firmware_versions = list(
        devices.values_list(
            'firmware_version',
            flat=True
        )
    )
    context = {
        'total_cattle': total_cattle,
        'total_readings': total_readings,
        'avg_temp': avg_temp,
        'avg_heart_rate': avg_heart_rate,
        'avg_milk': avg_milk,
        'activity_labels': list(activity_data.keys()),
        'activity_values': list(activity_data.values()),
        'temp_labels': temp_labels,
        'temp_values': temp_values,
        'heart_values': heart_values,
        'milk_values': milk_values,
        'battery_values': battery_values,
        'high_temp_count': high_temp_count,
        'low_activity_count': low_activity_count,
        'critical_battery_count': critical_battery_count,
        'abnormal_heart_rate': abnormal_heart_rate,
        'ai_health_score': ai_health_score,
        'total_devices': devices.count(),
        'online_devices': online_devices,
        'offline_devices': offline_devices,
        'low_battery_devices': low_battery_devices,
        'firmware_versions': firmware_versions,
    }
    return render(
        request,
        'analytics_dashboard/dashboard.html',
        context
    )

@login_required
def device_diagnostics(request):
    if not analytics_access(request.user):
        return render(request, '403.html')
    readings = SensorReading.objects.all().order_by('-timestamp')
    devices = Device.objects.all()
    context = {
        'devices': devices,
        'readings': readings[:50],
    }
    return render(
        request,
        'analytics_dashboard/device_diagnostics.html',
        context
    )