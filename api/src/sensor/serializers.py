from rest_framework import serializers
from .models import Sensor


class SensorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id']


class SensorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'license']
        depth = 3
