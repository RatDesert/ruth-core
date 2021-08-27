from django.urls import include, path
from django.conf.urls import url
from rest_framework_nested import routers
from .views import RegisterViewset, UserView


router = routers.SimpleRouter()
router.register(r'register', RegisterViewset, basename='register')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'user/', UserView.as_view(), name='user')
]
