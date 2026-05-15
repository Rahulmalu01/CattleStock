import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.conf import settings
from .models import (Device, Cattle, SensorReading)
from cattlestock.mongodb import alerts_collection

@csrf_exempt
def sensor_data_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)
    try:
        api_key = request.headers.get('X-API-KEY')
        if api_key != settings.HARDWARE_API_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        data = json.loads(request.body)
        device_data = data['device']
        device, _ = Device.objects.get_or_create(
            device_id=device_data['device_id'],
            defaults={
                'device_name': device_data['device_name'],
                'device_type': device_data['device_type'],
                'firmware_version': device_data['firmware_version'],
            }
        )
        cattle_data = data['cattle']
        cattle, _ = Cattle.objects.get_or_create(
            cattle_id=cattle_data['cattle_id'],
            defaults={'rfid_tag': cattle_data['rfid_tag']}
        )
        readings = data['readings']
        vital = readings['vital_signs']
        activity = readings['activity']
        rumination = readings['rumination']
        behavior = readings['behavior']
        milk = readings['milk']
        feeding = readings['feeding']
        device_status = data['device_status']
        quality = data['data_quality']
        SensorReading.objects.create(
            device=device,
            cattle=cattle,
            timestamp=parse_datetime(data['timestamp']),
            body_temperature=vital['body_temperature'],
            heart_rate=vital['heart_rate'],
            respiratory_rate=vital['respiratory_rate'],
            steps=activity['steps'],
            activity_duration_minutes=activity['activity_duration_minutes'],
            activity_level=activity['activity_level'],
            rumination_duration_minutes=rumination['rumination_duration_minutes'],
            rumination_episodes=rumination['rumination_episodes'],
            rumination_quality=rumination['rumination_quality'],
            eating_duration_minutes=behavior['eating_duration_minutes'],
            lying_duration_minutes=behavior['lying_duration_minutes'],
            standing_duration_minutes=behavior['standing_duration_minutes'],
            walking_duration_minutes=behavior['walking_duration_minutes'],
            milk_yield_liters=milk['milk_yield_liters'],
            milk_conductivity=milk['milk_conductivity'],
            feeding_efficiency_percent=feeding['feeding_efficiency_percent'],
            feed_intake_estimated=feeding['feed_intake_estimated'],
            battery_level_percent=device_status['battery_level_percent'],
            signal_strength_percent=device_status['signal_strength_percent'],
            gps_accuracy=device_status['gps_accuracy'],
            quality_score=quality['quality_score'],
            data_points_received=quality['data_points_received'],
            data_points_expected=quality['data_points_expected'],
        )
        return JsonResponse({
            'success': True,
            'message': 'Sensor data stored successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
def alert_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)
    try:
        api_key = request.headers.get('X-API-KEY')
        if api_key != settings.HARDWARE_API_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        data = json.loads(request.body)
        data['received_at'] = datetime.utcnow()
        alerts_collection.insert_one(data)
        return JsonResponse({
            'success': True,
            'message': 'Alert stored successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def latest_sensor_data(request):
    readings = SensorReading.objects.order_by('-timestamp')[:50]
    data = []
    for reading in readings:
        data.append({
            'cattle_id': reading.cattle.cattle_id,
            'rfid_tag': reading.cattle.rfid_tag,
            'temperature': reading.body_temperature,
            'heart_rate': reading.heart_rate,
            'activity_level': reading.activity_level,
            'battery': reading.battery_level_percent,
            'timestamp': reading.timestamp,
        })
    return JsonResponse({'readings': data})

def latest_alerts(request):
    alerts = list(
        alerts_collection.find()
        .sort('created_at', -1)
        .limit(20)
    )
    for alert in alerts:
        alert['_id'] = str(alert['_id'])
    return JsonResponse({'alerts': alerts})