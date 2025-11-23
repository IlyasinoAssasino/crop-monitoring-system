from django.db import models
from django.contrib.auth.models import User

class FarmProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    size = models.FloatField(help_text="Size in hectares")
    crop_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FieldPlot(models.Model):
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='plots')
    name = models.CharField(max_length=100)
    crop_variety = models.CharField(max_length=100)
    size = models.FloatField(help_text="Size in hectares")
    location_coordinates = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.name, self.crop_variety)

class SensorReading(models.Model):
    SENSOR_TYPES = [
        ('moisture', 'Soil Moisture'),
        ('temperature', 'Air Temperature'),
        ('humidity', 'Humidity'),
    ]
    
    plot = models.ForeignKey(FieldPlot, on_delete=models.CASCADE, related_name='readings')
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default='simulator')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return "{} - {}: {}".format(self.plot.name, self.sensor_type, self.value)



class AnomalyEvent(models.Model):
    ANOMALY_TYPES = [
        ('moisture_drop', 'Moisture Drop'),
        ('temperature_high', 'High Temperature'),
        ('humidity_low', 'Low Humidity'),
        ('sensor_drift', 'Sensor Drift'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    plot = models.ForeignKey(FieldPlot, on_delete=models.CASCADE, related_name='anomalies')
    anomaly_type = models.CharField(max_length=20, choices=ANOMALY_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    detected_at = models.DateTimeField(auto_now_add=True)
    model_confidence = models.FloatField(help_text="Confidence score from ML model")
    
    def __str__(self):
        return "{} - {} ({})".format(self.plot.name, self.anomaly_type, self.severity)


class AgentRecommendation(models.Model):
    anomaly_event = models.ForeignKey(AnomalyEvent, on_delete=models.CASCADE, related_name='recommendations')
    recommended_action = models.CharField(max_length=200)
    explanation_text = models.TextField()
    confidence = models.CharField(max_length=20)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Recommendation for {}".format(self.anomaly_event)