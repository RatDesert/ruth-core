import requests
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from .models import Hub


@shared_task
def notify_hub_registration(user_id, hub_name, hub_id, ipv4):
    url = settings.NOTIFICATIONS_SERVICE_URL
    headers = {
        settings.NOTIFICATIONS_SERVICE_API_KEY_HEADER: settings.NOTIFICATIONS_SERVICE_API_KEY}

    data = {'user_id': user_id, 'handler': 'registred', 'target': 'hub',
            'tittle': f'New hub was added: {hub_name}', 'type': 'info', 'details': {'hub_id': hub_id, 'ipv4': ipv4}, 'timestamp': datetime.timestamp(timezone.now())}
    r = requests.post(url, json=data, headers=headers)
    print(r.text)
