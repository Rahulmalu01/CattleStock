from django.db import models

class Device(models.Model):
    DEVICE_TYPES = (
        ('collar', 'Collar'),
        ('ear_tag', 'Ear Tag'),
    )
    device_id = models.CharField(max_length=100,unique=True)
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=50,choices=DEVICE_TYPES)
    firmware_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.device_name

class Cattle(models.Model):
    cattle_id = models.CharField(max_length=100,unique=True)
    rfid_tag = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cattle_id

class SensorReading(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    cattle = models.ForeignKey(Cattle,on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    body_temperature = models.FloatField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    steps = models.IntegerField()
    activity_duration_minutes = models.IntegerField()
    activity_level = models.CharField(max_length=50)
    rumination_duration_minutes = models.IntegerField()
    rumination_episodes = models.IntegerField()
    rumination_quality = models.CharField(max_length=50)
    eating_duration_minutes = models.IntegerField()
    lying_duration_minutes = models.IntegerField()
    standing_duration_minutes = models.IntegerField()
    walking_duration_minutes = models.IntegerField()
    milk_yield_liters = models.FloatField()
    milk_conductivity = models.FloatField()
    feeding_efficiency_percent = models.FloatField()
    feed_intake_estimated = models.BooleanField()
    battery_level_percent = models.IntegerField()
    signal_strength_percent = models.IntegerField()
    gps_accuracy = models.CharField(max_length=50)
    quality_score = models.CharField(max_length=50)
    data_points_received = models.IntegerField()
    data_points_expected = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.cattle.cattle_id} - {self.timestamp}'