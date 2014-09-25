import logging

from celery import shared_task

from django.core.mail import send_mail
from abdcp_adapter import settings

@shared_task
def send_email(info):
    send_mail(info["subject"], info["body"], settings.SENDER_EMAIL,
    [info["to"]], fail_silently=False)