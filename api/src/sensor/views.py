from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins
from jwt_auth import authentication
from hub.models import Hub
from .models import Sensor
from .serializers import SensorListSerializer, SensorRetrieveSerializer
from .permisions import IsOwner


class SensorViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_action_classes = {
        'list': SensorListSerializer,
        'retrieve': SensorRetrieveSerializer,
    }
    lookup_value_regex = '[0-9]+'

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action)

    def get_queryset(self):
        """Returns list of sensors that belongs to requested and owned hub or 404"""
        hub_pk = self.kwargs['hub_pk']
        # this query was chosen to separate "user has the resource but no entities [200]" and "user has no resource[404]"

        try:
            hub_pk = int(hub_pk)
            hub = get_object_or_404(Hub.objects.select_related('license__model'), pk=hub_pk)
        except ValueError:
            hub = get_object_or_404(Hub.objects.select_related('license__model'), name=hub_pk)
            
        self.check_object_permissions(self.request, hub)
        return Sensor.objects.filter(hub=hub)

    def get_object(self):
        """Returns requested sensor or 404"""
        sensor_pk = self.kwargs['pk']
        queryset = self.get_queryset()
        # get_queryset already checked obj permission
        sensor = get_object_or_404(
            queryset.select_related('license__model'), pk=sensor_pk)
        return sensor
