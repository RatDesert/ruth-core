import secrets
import inspect
import random
from uuid import uuid4
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from .models import HubModel, HubLicense, Hub

User = get_user_model()


class HubAPI(APITestCase):

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

        create_users()
        create_hubs()

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

    def test_create(self):
        user = HubAPI.users[0]
        model = HubModel.objects.get(name='smrt')
        license = HubLicense.objects.create(
            model=model, is_used=False)
        url = '/api/hubs/'
        data = {"key": license.key, "name": "test_name"}
        self._base_test(url, "POST", 201, user=user, data=data)
        self._base_test(url, "POST", 400, user=user, data=data)

        data = {"key": uuid4(), "name": "test_name"}
        self._base_test(url, "POST", 400, user=user, data=data)

    def test_list(self):
        user = HubAPI.users[0]
        url = '/api/hubs/'
        self._base_test(url, "GET", 200, user=user)

    def test_retrieve(self):
        user = HubAPI.users[0]
        hub = Hub.objects.filter(user=user).first()
        url = '/api/hubs/{}/'.format(hub.id)
        self._base_test(url, "GET", 200, user=user)

    def test_update(self):
        user = HubAPI.users[0]
        hub = Hub.objects.filter(user=user).first()
        url = '/api/hubs/{}/'.format(hub.id)
        data = {'name': "test_name"}
        self._base_test(url, "PUT", 200, user=user, data=data)
        hub.refresh_from_db()
        self.assertEqual(hub.name, "test_name",
                         'Expected hub.name: "{}", received "{}" instead.'
                         .format("test_name", hub.name))
