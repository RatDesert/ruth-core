import secrets
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, exceptions, status
from rest_framework.fields import CharField, UUIDField
from .models import Hub, HubLicense
from .exceptions import Conflict
from .tasks import notify_hub_registration


class HubCreateSerializer(serializers.Serializer):
    """Registers the hub if the license key is valid."""

    key = UUIDField(write_only=True)

    def validate(self, data):
        try:
            license = HubLicense.objects.get(
                key=data.pop('key'))

            if hasattr(license, 'hub'):
                raise serializers.ValidationError({'key': 'already used'})

            data['license'] = license
            return data

        except HubLicense.DoesNotExist:
            raise serializers.ValidationError({'key': 'does not exist'})

    def create(self, validated_data):
        """Creates a hub with the generated password
           and changes the license state for the used one."""
        raw_pwd = secrets.token_hex(32)
        hashed_pwd = make_password(raw_pwd)
        hub = Hub.objects.create(**validated_data, password=hashed_pwd)
        ipv4 = self.context.get('request').META.get("REMOTE_ADDR")
        notify_hub_registration.delay(hub.user.id, hub.name, hub.id, ipv4)
        data = {"password": raw_pwd}
        return data


class HubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = ['name', 'id']


class HubRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = ['license']
        depth = 2


class HubUpdateSerializer(serializers.Serializer):
    name = CharField(min_length=4, max_length=128, write_only=True)

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance
        except IntegrityError as e:

            if 'unique constraint' in e.args[0]:
                raise Conflict(
                    detail={'name': 'must be unique'})

            raise e


# special serializer for m2m API only
