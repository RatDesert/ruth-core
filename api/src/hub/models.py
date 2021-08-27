from uuid import uuid4
from django.db import models
from django.conf import settings


class HubModel(models.Model):
    """Stores a hub model description for license"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)

    class Meta:
        db_table = 'hub_models'


class HubLicense(models.Model):
    """Stores a license for hub registration"""
    id = models.AutoField(primary_key=True)
    key = models.UUIDField(default=uuid4)
    model = models.ForeignKey(HubModel, on_delete=models.PROTECT)

    class Meta:
        db_table = 'hub_licenses'


class Hub(models.Model):
    """Stores hub description"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, default=uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hubs')
    password = models.TextField()
    license = models.OneToOneField(HubLicense, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hubs'
        constraints = [models.UniqueConstraint(fields=['user', 'name'], name="%(class)s_unique_name_per_user")]
