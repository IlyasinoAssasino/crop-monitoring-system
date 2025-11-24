from django.contrib import admin
from .models import FarmProfile, FieldPlot, SensorReading, AnomalyEvent, AgentRecommendation

@admin.register(FarmProfile)
class FarmProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'size', 'crop_type', 'created_at']
    list_filter = ['crop_type', 'created_at']
    search_fields = ['name', 'location']

@admin.register(FieldPlot)
class FieldPlotAdmin(admin.ModelAdmin):
    list_display = ['name', 'farm', 'crop_variety', 'size']
    list_filter = ['farm', 'crop_variety']
    search_fields = ['name', 'crop_variety']

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['plot', 'sensor_type', 'value', 'timestamp']
    list_filter = ['sensor_type', 'timestamp']
    search_fields = ['plot__name']

@admin.register(AnomalyEvent)
class AnomalyEventAdmin(admin.ModelAdmin):
    list_display = ['plot', 'anomaly_type', 'severity', 'model_confidence', 'detected_at']
    list_filter = ['anomaly_type', 'severity', 'detected_at']
    search_fields = ['plot__name']

@admin.register(AgentRecommendation)
class AgentRecommendationAdmin(admin.ModelAdmin):
    list_display = ['anomaly_event', 'recommended_action', 'confidence', 'generated_at']
    list_filter = ['confidence', 'generated_at']
    search_fields = ['anomaly_event__plot__name']