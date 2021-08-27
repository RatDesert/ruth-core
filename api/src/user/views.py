from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status, permissions, views
from rest_framework.decorators import action
from .serializers import UserCreateSerializer, UsernameSeializer, EmailSerializer, EmailTokenSerializer, UserRetrieveSerializer
from .utils import create_email_token, get_activation_url, send_email_confirmation, activate_account
from .exceptions import EmailTokenNotValid
from .throttle import CheckUserAtributesThrottle, RegistrationThrottle
from jwt_auth import authentication


class RegisterViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Registers the user."""
    serializer_action_classes = {
        'create': UserCreateSerializer,
    }

    throttle_action_classes = {
        'create': [RegistrationThrottle]
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action)

    def get_throttles(self):
        throttles = self.throttle_action_classes.get(self.action, [])
        return [throttle() for throttle in throttles]

    def perform_create(self, serializer):
        user = serializer.save()
        token = create_email_token(user)
        activation_url = get_activation_url(
            token, 'register-activate-account', self.request)
        send_email_confirmation(user, activation_url)

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED, data={'detail': 'Please check email to confirm your registration'})

    @action(detail=False, methods=['post'], throttle_classes=[CheckUserAtributesThrottle])
    def check_username(self, request):
        serializer = UsernameSeializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=['post'], throttle_classes=[CheckUserAtributesThrottle])
    def check_email(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def activate_account(self, request):
        try:
            token = self.request.query_params.get("token")
            serializer = EmailTokenSerializer(data={'token': token})

            if serializer.is_valid():
                token = serializer.validated_data['token']
                activate_account(token)
                query = '/?alert=email_confirmation&type=success'
                # must redirect to view with message
                return HttpResponseRedirect(redirect_to=settings.FRONTEND_DOMAIN_NAME + query)
            else:
                raise EmailTokenNotValid

        except EmailTokenNotValid:
            query = '/?alert=email_confirmation&type=error'
            # must redirect to view with message
            return HttpResponseRedirect(redirect_to=settings.FRONTEND_DOMAIN_NAME + '/login' + query)

    # def resend_activation_mail
    # def password_reset


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get(self, request):
        serializer = UserRetrieveSerializer(request.user)
        return Response(serializer.data)
