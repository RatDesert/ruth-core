from rest_framework import throttling


class CheckUserAtributesThrottle(throttling.AnonRateThrottle):
    rate = '1/second'
    scope = "check"

class RegistrationThrottle(throttling.AnonRateThrottle):
    rate = '30/minute'
    scope = "register"