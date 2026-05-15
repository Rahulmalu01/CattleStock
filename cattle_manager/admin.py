from django.contrib import admin
from .models import (Farm, CattleProfile)

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'owner',
        'total_cattle',
    )

@admin.register(CattleProfile)
class CattleProfileAdmin(admin.ModelAdmin):
    list_display = (
        'cattle_id',
        'name',
        'breed',
        'health_status',
        'last_temperature',
        'last_heart_rate',
    )
    list_filter = (
        'health_status',
        'breed',
    )