from django.contrib import admin
from .models import (Device, Cattle, SensorReading)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'device_id',
        'device_name',
        'device_type',
        'firmware_version',
    )

@admin.register(Cattle)
class CattleAdmin(admin.ModelAdmin):
    list_display = (
        'cattle_id',
        'rfid_tag',
    )

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = (
        'cattle',
        'body_temperature',
        'heart_rate',
        'activity_level',
        'battery_level_percent',
        'timestamp',
    )
    list_filter = (
        'activity_level',
        'quality_score',
    )
    search_fields = (
        'cattle__cattle_id',
        'cattle__rfid_tag',
    )