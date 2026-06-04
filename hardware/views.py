import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from hardware.models import Device, Cattle, SensorReading
from cattle_manager.models import CattleProfile
from cattlestock.mongodb import alerts_collection
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from prediction.tasks import create_prediction

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
        sensor_reading = SensorReading.objects.create(
            device=device,
            cattle=cattle,
            timestamp=timezone.now(),
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

        try:
            create_prediction(cattle,sensor_reading)
        except Exception as prediction_error:
            print(f"Prediction Error: {prediction_error}")

        health_status = 'healthy'
        if vital['body_temperature'] >= 40 or vital['heart_rate'] > 100 or activity['activity_level'] == 'low' or device_status['battery_level_percent'] < 20:
            health_status = 'warning'
        if vital['body_temperature'] >= 41 or vital['heart_rate'] > 110 or device_status['battery_level_percent'] < 10:
            health_status = 'critical'

        CattleProfile.objects.filter(cattle_id=cattle_data['cattle_id']).update(
            last_temperature=vital['body_temperature'],
            last_heart_rate=vital['heart_rate'],
            last_activity=activity['activity_level'],
            health_status=health_status,
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'monitoring',
            {
                'type': 'sensor_update',
                'data': {
                    'cattle_id': cattle_data['cattle_id'],
                    'rfid_tag': cattle_data['rfid_tag'],
                    'temperature': vital['body_temperature'],
                    'heart_rate': vital['heart_rate'],
                    'activity_level': activity['activity_level'],
                    'battery': device_status['battery_level_percent'],
                    'timestamp': timezone.now().isoformat(),
                }
            }
        )

        total_cattle = CattleProfile.objects.count()
        healthy = CattleProfile.objects.filter(health_status='healthy').count()
        warning = CattleProfile.objects.filter(health_status='warning').count()
        critical = CattleProfile.objects.filter(health_status='critical').count()
        async_to_sync(channel_layer.group_send)(
            'monitoring',
            {
                'type': 'status_update',
                'data': {
                    'total_cattle': total_cattle,
                    'healthy': healthy,
                    'warning': warning,
                    'critical': critical,
                }
            }
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

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'monitoring',
            {
                'type': 'alert_update',
                'data': {
                    'title': data.get('title', 'Alert'),
                    'description': data.get('description', ''),
                    'severity': data.get('severity', 'medium'),
                    'cattle_id': data.get('cattle_id'),
                    'created_at': data['received_at'].isoformat(),
                }
            }
        )

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