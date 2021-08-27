import re
from rest_framework import serializers, fields
from rest_framework.validators import UniqueValidator
from .models import User

USERNAME_RE = re.compile(r"^(?!.*\.\.)(?!.*\.$)[^\W][\w.]*$")
            

class UserCreateSerializer(serializers.Serializer):
    username = fields.RegexField(USERNAME_RE, min_length=4, max_length=64, write_only=True, validators=[
        UniqueValidator(queryset=User.objects.all(), message='Username is already taken')])
    email = fields.EmailField(write_only=True, validators=[
        UniqueValidator(queryset=User.objects.all(), message='Email already used')])
    # https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
    password = fields.CharField(min_length=8, max_length=64, write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserRetrieveSerializer(serializers.Serializer):
    id = fields.UUIDField(read_only=True)
    username = fields.CharField(read_only=True)
    email = fields.EmailField(read_only=True)


class UsernameSeializer(serializers.Serializer):
    username = fields.CharField(min_length=4, max_length=64, write_only=True)
    is_available = fields.SerializerMethodField()

    def get_is_available(self, obj):
        return not User.objects.filter(**obj).exists()

class EmailSerializer(serializers.Serializer):
    email = fields.EmailField(write_only=True)
    is_available = fields.SerializerMethodField()

    def get_is_available(self, obj):
        return not User.objects.filter(**obj).exists()

class EmailTokenSerializer(serializers.Serializer):
    token = fields.CharField(min_length=32, max_length=64)