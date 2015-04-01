import logging
import requests
import json
import base64

from celery import shared_task
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from abdcp_messages.models import ABDCPMessage
from abdcp_adapter import settings

@shared_task
def send_email(info):
    t = get_template("itp_notification.html")
    c=Context(info)
    body = t.render(c)
    msg = EmailMessage(info["subject"], body, settings.SENDER_EMAIL,[info["to"]])
    msg.content_subtype = "html"
    msg.send()


@shared_task
def send_message(message_id):
    retry = False
    try:
        logging.info("=== Begin ABDCP message send (%s)===" % message_id)
        message = ABDCPMessage.objects.get(message_id=message_id)
        result = ""

	payload = {
            "userID" : settings.ABDCP_CLIENT_REST_ADAPTER_USR,
            "password" : base64.b64encode(settings.ABDCP_CLIENT_REST_ADAPTER_PWD),
            "xmlMsg" : message.request_document,
            "attachedDoc" : None 
        }

	r = requests.post(settings.ABDCP_CLIENT_REST_ADAPTER_ENDPOINT, 
                          data=json.dumps(payload), verify=settings.ABDCP_CLIENT_REST_ADAPTER_VERIFY_SSL,
                          headers={
                             'Accept':'application/json',
                             'Content-Type':'application/json; charset=utf-8' 
                          }
        )

        print r.text
        if r.status_code == requests.codes.ok:

            response = json.loads(r.text)
            
            if "response" in response and response['response'][0:3]=='ERR':
                result = response['response']
            else:
                result = "Message %s (%s) has been sent" % \
                    (message.message_id,message.message_type)
            
                message.mark_delivered()
        else:
            result = "Message %s (%s) has NOT been sent, only stored\nError: %s"%\
                (message.message_id,message.message_type, r.raise_for_status())
    except ABDCPMessage.DoesNotExist, e:
        result = "message id %s was not found" % message_id
    except Exception, e:
        result = "Error: processing message %s %s" % (message.message_id,e)
        retry = True

    logging.info(result)

    if retry:
        send_message.retry(
            [message_id] ,
            max_retries = settings.CELERY_MAX_RETRIES,
            countdown=settings.CELERY_COUNTDOWN
        )

    logging.info("=== End ABDCP message sent ===")

    return result 
