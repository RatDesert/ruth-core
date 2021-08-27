from django.db import models
from django.contrib.auth import get_user_model
from django.utils import crypto, timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

User = get_user_model()


def generate_random_string():
    return crypto.get_random_string(32)


def get_refresh_expire_date():
    return timezone.now() + settings.REFRESH_MAX_AGE


class RefreshSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_key = models.CharField(max_length=40,
                                   default=generate_random_string)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='refresh_sessions')
    expire_date = models.DateTimeField(default=get_refresh_expire_date)
    http_user_agent = models.TextField(null=True)
    remote_addr = models.GenericIPAddressField(null=True)
    remote_host = models.TextField(null=True)

    class Meta:
        db_table = 'refresh_sessions'


@receiver(post_save, sender=RefreshSession)
def session_limit_reached(sender, instance, created, **kwargs):
    if created:
        q = RefreshSession.objects.filter(user=instance.user)
        if len(q) >= 6:
            q.filter(~Q(id=instance.id)).delete()
