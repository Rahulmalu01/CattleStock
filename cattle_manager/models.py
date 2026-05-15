from django.db import models
from hardware.models import Device

class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    owner = models.CharField(max_length=100)
    total_cattle = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class CattleProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    HEALTH_STATUS = (
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    )
    cattle_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=200)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.FloatField()
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    farm = models.ForeignKey(Farm,on_delete=models.CASCADE)
    device = models.OneToOneField(Device,on_delete=models.SET_NULL,null=True,blank=True)
    health_status = models.CharField(max_length=20,choices=HEALTH_STATUS,default='healthy')
    last_temperature = models.FloatField(default=0)
    last_heart_rate = models.IntegerField(default=0)
    last_activity = models.CharField(max_length=50,default='normal')
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class FarmStaff(models.Model):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('cattle_manager', 'Cattle Manager'),
    )
    user = models.ForeignKey('accounts.Account',on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm,on_delete=models.CASCADE)
    role = models.CharField(max_length=30,choices=ROLE_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)