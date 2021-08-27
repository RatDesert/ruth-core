from django.urls import include, path
from rest_framework_nested import routers
from .views import HubViewset


hub_router = routers.SimpleRouter()
hub_router.register(r'hubs', HubViewset, basename='hubs')

urlpatterns = [
    path('', include(hub_router.urls)),
]
