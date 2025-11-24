from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import FarmProfile, FieldPlot, SensorReading, AnomalyEvent, AgentRecommendation
from .serializers import (
    FarmProfileSerializer,
    FieldPlotSerializers,
    SensorReadingSerializer,
    AnomalyEventSerializer,
    AgentRecommendationSerializer
)

# Custom permission to ensure access is restricted to the owner or admins
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        if hasattr(obj, "farm"):
            return obj.farm.owner == request.user
        return False

# Base class for filtering ViewSets by owner
class OwnerFilteredMixin:
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if not user.is_superuser:
            if hasattr(queryset.model, "owner"):
                queryset = queryset.filter(owner=user)
            elif hasattr(queryset.model, "farm"):
                queryset = queryset.filter(farm__owner=user)
        return queryset

# FarmProfile ViewSet
class FarmProfileViewSet(OwnerFilteredMixin, viewsets.ModelViewSet):
    queryset = FarmProfile.objects.all()
    serializer_class = FarmProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_superuser:
            serializer.save(owner=user)  # Save the current user as the owner
        else:
            serializer.save()  # Admins can manually assign the owner

# FieldPlot ViewSet
class FieldPlotViewSet(OwnerFilteredMixin, viewsets.ModelViewSet):
    queryset = FieldPlot.objects.all()
    serializer_class = FieldPlotSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_superuser:
            farm = FarmProfile.objects.get(owner=user)  # Auto-assign the farm of the logged-in user
        else:
            farm_id = self.request.data.get('farm')  # Admins can assign the farm manually
            farm = FarmProfile.objects.get(id=farm_id)  # Admin can choose any farm
        serializer.save(farm=farm)

# SensorReading ViewSet
class SensorReadingViewSet(OwnerFilteredMixin, viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        plot_id = self.request.query_params.get("plot")
        if plot_id:
            queryset = queryset.filter(plot_id=plot_id)
        return queryset

# AnomalyEvent ViewSet (read-only)
class AnomalyEventViewSet(OwnerFilteredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = AnomalyEvent.objects.all()
    serializer_class = AnomalyEventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# AgentRecommendation ViewSet (read-only)
class AgentRecommendationViewSet(OwnerFilteredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = AgentRecommendation.objects.all()
    serializer_class = AgentRecommendationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
