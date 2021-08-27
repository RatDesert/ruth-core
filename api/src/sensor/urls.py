from django.urls import include, path
from rest_framework_nested import routers
from hub.urls import hub_router
from .views import SensorViewset

#Nested urls design. Example: api/hubs/{pk}/sensors/{pk}
sensor_nested_router = routers.NestedSimpleRouter(
    hub_router, r'hubs', lookup='hub')
sensor_nested_router.register(r'sensors', SensorViewset, basename='sensors')

urlpatterns = [
    path('', include(sensor_nested_router.urls)),
]
