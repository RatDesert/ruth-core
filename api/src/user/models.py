import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser):
    """
    Custom User model with two permission groups.
    """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=64)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'users'
        constraints = [
            # Superuser is always staff
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_superuser_is_staff",
                check=(
                    ~models.Q(
                        is_superuser=True,
                        is_staff=False
                    )
                )
            )
        ]

    def __str__(self):
        return self.username

def generate_email_token():
    return  secrets.token_urlsafe(32)

class EmailTokenWhitelist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_activation_token')
    token = models.CharField(max_length=64, default=generate_email_token)
    exp_date = models.DateTimeField()

    class Meta:
        db_table = 'whitelisted_email_tokens'
