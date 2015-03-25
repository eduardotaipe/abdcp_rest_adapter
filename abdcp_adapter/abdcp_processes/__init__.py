# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from requests_portability import PortabilityAPI
from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError

from abdcp_adapter.utils import load_class
from abdcp_adapter import settings
from abdcp_messages import constants
from abdcp_messages.tasks import send_message


class ABDCP_Message(object):
    notify_to = settings.ITP_CONTACT_EMAIL
    template = None

    def __init__(self, message=None):
        self.message = message
        self.set_xmlmodel()

    def get_xmlmodel_class(self):
        return getattr(self, 'xmlmodel_class', None)

    def generate_data(self):
        return {
            "subject":"Mensaje %s" % self.__class__.__name__,
            "detail": "Mensaje %s" % self.__class__.__name__
        }
        
    def notify(self):
        if self.template == None:
            self.template = "%s.html"%self.__class__.__name__
        
        data = self.generate_data()
        self.send_mail(data)

    def send_mail(self,data):
        t = get_template(self.template)
        c=Context(data)
        body = t.render(c)
        msg = EmailMessage(data["subject"], body, settings.SENDER_EMAIL,[self.notify_to])
        msg.content_subtype = "html"
        msg.send()

    def notify_ABDCP(self):
        send_message.delay(self.message.message_id)
        

    def process(self):
        self.notify()

    def set_xmlmodel(self):
        xmlstr = str(self.message.request_document)
        xmlmodel_class = self.get_xmlmodel_class()
        if xmlmodel_class is not None:
            self.xmlmodel = self.xmlmodel_class.create_from_string(xmlstr)
        else:
            self.xmlmodel = None

    def set_api_client(self):
        try:
            self.api = PortabilityAPI(
                base_url=settings.PORTABILITY_API_BASE_URL,
                api_key=settings.PORTABILITY_API_KEY
            )
            return
        except ClientError,e:
            logging.error("set_api_cliente:client error")
        except APIError,e:
            logging.error("set_api_cliente:Api error")
        except AuthError,e:
            logging.error("Authentication error")
        self.api = None


    @classmethod
    def processor_factory(cls,message):
        process_type = \
            constants.ABDCP_PROCESS_CHOICES.get_key(message.process_type)
        message_type = message.message_type

        cls_path  = "abdcp_processes.%(process_type)s.%(message_type)s" 
        cls_path  = cls_path % {
            "process_type" : process_type.lower(),
            "message_type" : message_type
        }
        try:
            klass = load_class(cls_path)
            return klass(message=message)
        except (ValueError,ImportError):
            return None
