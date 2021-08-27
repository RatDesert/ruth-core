from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@shared_task
def send_email(email, message, subject):
    email = EmailMessage(subject, message, to=[email])
    email.send()