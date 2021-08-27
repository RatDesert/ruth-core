from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class Conflict(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _(
        'The request could not be completed due to a conflict with the current state of the target resource.')
    default_code = 'conflict'
