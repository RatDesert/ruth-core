from django.shortcuts import get_object_or_404
from .permissions import IsOwner
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from jwt_auth import authentication
from .models import Hub
from .serializers import (HubCreateSerializer, HubListSerializer,
                          HubRetrieveSerializer, HubUpdateSerializer)
from .tasks import notify_hub_registration

class HubViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_action_classes = {
        'list': HubListSerializer,
        'create': HubCreateSerializer,
        'update': HubUpdateSerializer,
        'retrieve': HubRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action)

    def get_queryset(self):
        user = self.request.user
        return Hub.objects.filter(user=user)

    def get_object(self):
        hub_pk = self.kwargs['pk']

        try:
            hub_pk = int(hub_pk)
            hub = get_object_or_404(Hub.objects.select_related('license__model'), pk=hub_pk)
        except ValueError:
            hub = get_object_or_404(Hub.objects.select_related('license__model'), name=hub_pk)

        self.check_object_permissions(self.request, hub)
        return hub

    def create(self, request):
        serializer = HubCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save(user=request.user)
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
