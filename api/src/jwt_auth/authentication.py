import jwt
from django.middleware.csrf import CsrfViewMiddleware
from django.core import signing
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')


class JWTAuthentication(authentication.BaseAuthentication):

    def enforce_csrf(self, request):
        csrf_check = CSRFCheck()
        csrf_check.process_request(request)
        reason = csrf_check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')

    def authenticate(self, request):
        # self.enforce_csrf(request)
        token = self.get_jwt(request)

        if token is None:
            return None

        payload = self.verify_jwt(token)
        return self.get_user(payload), token

    def get_jwt(self, request):
        return request.COOKIES.get(settings.ACCESS_COOKIE_NAME, None)

    def verify_jwt(self, token):
        # TODO: check if token in blacklist(REDIS)
        return self._decode_jwt(token)

    def get_user(self, payload):
        # TODO: return JWTUser(AnonymousUser) class
        user_id = payload['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'User does not exist', code='user_not_found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User is inactive', code='user_inactive')

        return user

    def authenticate_header(self, request):
        # in case of missing auth cookie
        return 'Cookie realm="api"'

    def _decode_jwt(self, token):
        try:
            payload = jwt.decode(token, settings.ACCESS_JWT_SIGNING_KEY, algorithms=[
                'HS256'], options={'verify_exp': True})

        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Access JWT has expired', code='access_token_expired')
        except (jwt.exceptions.InvalidTokenError):
            raise exceptions.AuthenticationFailed(
                'Access JWT is invalid ', code='access_token_not_valid')

        if payload['token_type'] != 'access':
            raise exceptions.AuthenticationFailed(
                'Access JWT is invalid', code='access_token_not_valid')

        return payload


class RefreshAuthentication(authentication.BaseAuthentication):

    def enforce_csrf(self, request):
        csrf_check = CSRFCheck()
        csrf_check.process_request(request)
        reason = csrf_check.process_view(request, None, (), {})

        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')

    def authenticate(self, request):
        # self.enforce_csrf(request)

        try:
            session_key = request.get_signed_cookie(
                settings.REFRESH_COOKIE_NAME, salt=settings.REFRESH_COOKIE_SALT, max_age=settings.REFRESH_MAX_AGE)
        except (KeyError, signing.BadSignature, signing.SignatureExpired):
            return None

        return self.get_user(session_key)

    def get_user(self, session_key):
        try:
            user = User.objects.prefetch_related('refresh_sessions').get(
                refresh_sessions__session_key=session_key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'User does not exist', code='user_not_found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User is inactive', code='user_inactive')

        return (user, user.refresh_sessions.filter(session_key=session_key)[0])

    def authenticate_header(self, request):
        return 'Cookie realm="api/auth"'
