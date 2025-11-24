from rest_framework import serializers
from .models import FarmProfile, FieldPlot, SensorReading, AnomalyEvent, AgentRecommendation
from django.contrib.auth.models import User  # Import User to reference the logged-in user

class FarmProfileSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)  # Visible for GET, non-modifiable for POST/PUT

    class Meta:
        model = FarmProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'owner']  # `owner` will be auto-assigned and not modifiable

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_superuser:
            validated_data['owner'] = user  # Owner is the current user for normal users
        return super().create(validated_data)


class FieldPlotSerializers(serializers.ModelSerializer):
    # Farm is auto-assigned to the logged-in user for regular users
    farm = serializers.PrimaryKeyRelatedField(queryset=FarmProfile.objects.all(), required=False, write_only=True)

    class Meta:
        model = FieldPlot
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user

        # If the user is not an admin, auto-assign the `FieldPlot` to their farm
        if not user.is_superuser:
            farm = FarmProfile.objects.filter(owner=user).first()
            if farm:
                validated_data['farm'] = farm
            else:
                raise serializers.ValidationError("No farm found for this user.")
        return super().create(validated_data)


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'


class AnomalyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyEvent
        fields = '__all__'
        read_only_fields = ['detected_at']  # `detected_at` is read-only


class AgentRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentRecommendation
        fields = '__all__'
        read_only_fields = ['generated_at']  # `generated_at` is read-only
