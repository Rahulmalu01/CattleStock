from django.contrib import admin
from prediction.models import DiseasePrediction

@admin.register(DiseasePrediction)
class DiseasePredictionAdmin(admin.ModelAdmin):
    list_display = ('cattle','disease','confidence','risk_level','created_at')
    search_fields = ('cattle__name','disease')