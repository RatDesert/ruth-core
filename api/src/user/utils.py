from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse
from .models import EmailTokenWhitelist
from .exceptions import EmailTokenNotValid
from .tasks import send_email

TOKEN_LIFETIME = timezone.timedelta(days=14)


def create_email_token(user):
    exp_date = timezone.now() + TOKEN_LIFETIME
    token = EmailTokenWhitelist.objects.create(user=user, exp_date=exp_date)
    return token.token

def get_activation_url(token, view_name, request):
    url = reverse(view_name, request=request)
    return f"{url}?token={token}"


def send_email_confirmation(user, activate_url):
    
    message = render_to_string('email_user_activation.html', {
        'user': user,
        'url': activate_url,
    })
    email_subject = 'Activate your account.'
    send_email.delay(user.email, message, email_subject)


def activate_account(token):
    try:
        token = EmailTokenWhitelist.objects.select_related('user').get(token=token)

        if timezone.now() > token.exp_date:
            raise EmailTokenNotValid
    
        user = token.user
        user.is_active = True
        user.save()
        token.delete()
    except EmailTokenWhitelist.DoesNotExist:
        raise EmailTokenNotValid

