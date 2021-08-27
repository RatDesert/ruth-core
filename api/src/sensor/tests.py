import secrets
import inspect
import random
from django.db.models import Max
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from hub.models import HubModel, HubLicense, Hub
from .models import SensorModel, SensorLicense, Sensor

User = get_user_model()


class SensorAPI(APITestCase):

    MESSAGE_COLORS = {2: '\033[92m', 4: '\033[93m', 'error': '\033[91m'}

    @classmethod
    def setUpTestData(cls):

        cls.users = []
        cls.hubs = []

        def create_users(quantity=2, email_pattern="aloe_{}@vera.com", username_pattern="user_{}"):
            for _ in range(quantity):

                user = User.objects.create_user(email=email_pattern.format(
                    _), password=secrets.token_hex(8), username=username_pattern.format(_))
                cls.users.append(user)

        def create_hubs(quantity_per_user=random.randint(1, 5), name='hub'):
            model = HubModel.objects.create(name='smrt')
            for user in cls.users:
                # every hub need license
                for _ in range(quantity_per_user):
                    license = HubLicense.objects.create(
                        model=model, is_used=True)
                    hub = Hub.objects.create(license=license, user=user,
                                             name=name)
                    cls.hubs.append(hub)

        def create_sensors(quantity_per_hub=random.randint(1, 5), name='sensor'):
            model = SensorModel.objects.create(
                name='sxs2_', max_val=100, min_val=10, type='temp', dimension='c')
            for hub in cls.hubs:
                for _ in range(quantity_per_hub):
                    license = SensorLicense.objects.create(
                        model=model, is_used=True)
                    Sensor.objects.create(license=license, hub=hub, name=name)

        create_users()
        create_hubs()
        create_sensors()

    def _base_test(self, url, method, expected_response, user=None, data=None):
        client = APIClient()
        client.force_authenticate(user=user)
        request = getattr(client, method.lower())
        response = request(url, data)
        try:
            self.assertEqual(response.status_code, expected_response,
                             '\033[91mExpected Response Code {}, received {} instead.\033[0m\n'
                             .format(expected_response, response.status_code))
            color = self.MESSAGE_COLORS[response.status_code // 100]
        except AssertionError as e:
            color = self.MESSAGE_COLORS['error']
            print(e)
        finally:

            print(
                f"{type(self).__name__}.{inspect.stack()[1].function}: {color}{response.status_code}: {response.data}\033[0m\n")

    def test_list_(self):
        user = SensorAPI.users[0]
        hub = Hub.objects.filter(user=user)[0]
        url = '/api/hubs/{}/sensors/'.format(hub.id)

        self._base_test(url, "GET", 200, user=user)

        self._base_test(url, "GET", 401)

        user = SensorAPI.users[1]
        self._base_test(url, "GET", 403, user=user)

    def test_retrieve(self):
        user = SensorAPI.users[0]
        hub = Hub.objects.filter(user=user)[0]
        sensor = Sensor.objects.filter(hub=hub)[0]

        user_403 = SensorAPI.users[1]
        sensor_404 = Sensor.objects.all().aggregate(Max('id'))['id__max']

        url = '/api/hubs/{}/sensors/{}/'.format(hub.id, sensor.id)

        self._base_test(url, "GET", 200, user=user)

        self._base_test(url, "GET", 401)

        self._base_test(url, "GET", 403, user=user_403)

        url = '/api/hubs/{}/sensors/{}/'.format(hub.id, sensor_404)
        self._base_test(url, "GET", 404, user=user)

    def test_update(self):
        user = SensorAPI.users[0]
        hub = Hub.objects.filter(user=user)[0]
        sensor = Sensor.objects.filter(hub=hub)[0]
        url = '/api/hubs/{}/sensors/{}/'.format(hub.id, sensor.id)
        data = {'name': "ddwd2"}
        self._base_test(url, "PUT", 200, user=user, data=data)
