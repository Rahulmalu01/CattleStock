import requests
from django.conf import settings

def get_prediction(sensor_reading):
    payload = {
        "cattle_id": sensor_reading.cattle.cattle_id,
        "temperature": sensor_reading.body_temperature,
        "heart_rate": sensor_reading.heart_rate,
        "respiratory_rate": sensor_reading.respiratory_rate,
        "steps": sensor_reading.steps,
        "activity_level": sensor_reading.activity_level,
        "activity_duration_minutes": sensor_reading.activity_duration_minutes,
        "rumination_duration": sensor_reading.rumination_duration_minutes,
        "rumination_episodes": sensor_reading.rumination_episodes,
        "feeding_efficiency": sensor_reading.feeding_efficiency_percent,
        "milk_yield": sensor_reading.milk_yield_liters,
        "milk_conductivity": sensor_reading.milk_conductivity,
        "battery_level": sensor_reading.battery_level_percent,
        "signal_strength": sensor_reading.signal_strength_percent,
    }
    print("=" * 60)
    print("SENDING TO ML MODEL:")
    print(payload)
    print("=" * 60)
    response = requests.post(settings.PREDICTION_API_URL, json=payload, timeout=20)
    print("=" * 60)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("=" * 60)
    response.raise_for_status()
    return response.json()