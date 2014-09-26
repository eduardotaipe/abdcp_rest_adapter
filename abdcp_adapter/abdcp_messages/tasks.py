import logging

from celery import shared_task
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from abdcp_adapter import settings

@shared_task
def send_email(info):
    t = get_template("itp_notification.html")
    c=Context(info)
    body = t.render(c)
    msg = EmailMessage(info["subject"], body, settings.SENDER_EMAIL,[info["to"]])
    msg.content_subtype = "html"
    msg.send()