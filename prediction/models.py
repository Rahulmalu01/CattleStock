from django.db import models
from cattle_manager.models import CattleProfile

class DiseasePrediction(models.Model):
    DISEASE_CHOICES = [
        ('healthy', 'Healthy'),
        ('fever', 'Fever'),
        ('mastitis', 'Mastitis'),
        ('heat_stress', 'Heat Stress'),
        ('digestive_disorder', 'Digestive Disorder'),
    ]
    cattle = models.ForeignKey(CattleProfile, on_delete=models.CASCADE)
    disease = models.CharField(max_length=50, choices=DISEASE_CHOICES)
    confidence = models.FloatField()
    risk_level = models.CharField(max_length=20)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50,default='v1.0')
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.cattle.name} - {self.disease}"