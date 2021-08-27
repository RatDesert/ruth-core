from uuid import uuid4
from django.db import models
from hub.models import Hub


class SensorType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    dimension = models.CharField(max_length=128)

    class Meta:
        db_table = 'sensor_types'

class SensorModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    max_val = models.IntegerField()
    min_val = models.IntegerField()
    type = models.ForeignKey(SensorType, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sensor_models'


class SensorLicense(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.UUIDField(default=uuid4)
    model = models.ForeignKey(SensorModel, on_delete=models.PROTECT)

    class Meta:
        db_table = "sensor_licenses"


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    hub = models.ForeignKey(
        Hub, on_delete=models.CASCADE, related_name='sensors')
    license = models.OneToOneField(
        SensorLicense, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sensors'
