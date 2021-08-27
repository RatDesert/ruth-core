from django.conf import settings
from datetime import datetime
from uuid import uuid4
import jwt
from django.utils import timezone


def create_access_jwt(user):
    payload = {
        'token_type': 'access',
        'exp':  timezone.now() + settings.ACCESS_MAX_AGE,
        'jti': str(uuid4()),
        'user_id': user.id
    }
    token = jwt.encode(payload, settings.ACCESS_JWT_SIGNING_KEY,
                       algorithm='HS256').decode('utf-8')

    return token, datetime.utcfromtimestamp(payload['exp'])
