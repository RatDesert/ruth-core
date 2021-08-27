from django.urls import path, include


#nested api does not support schema

urlpatterns = [
    path('api/', include('user.urls')),
    path('api/auth/', include('jwt_auth.urls')),
    path('api/', include('hub.urls')),
    path('api/', include('sensor.urls')),
]
