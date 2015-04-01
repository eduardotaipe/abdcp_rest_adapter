# -*- coding: utf-8 -*-
import logging

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
from abdcp_messages import strings
from abdcp_messages.tasks import send_message
from abdcp_messages.models import ABDCPMessage
from operators.models import Operator

class ABDCP_Message(object):
    notify_to = settings.ITP_CONTACT_EMAIL
    template = None

    def __init__(self, message=None):
        self.message = message
        self.set_xmlmodel()

    def get_xmlmodel_class(self):
        return getattr(self, 'xmlmodel_class', None)
        
    def notify(self):
        if self.template == None:
            self.template = "%s.html"%self.__class__.__name__
        
        data = self.generate_data()
        self.send_mail(data)

    def send_mail(self,data):
        logging.info("Sending email to %s" % self.notify_to)
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

    def get_deep_number_info(self):
        process_type = self.message.process_type

        if process_type == '01':
            message_type = "ESC"
            
        elif process_type == '05':
            message_type = "ECPC"
        else:
            raise Exception("Invalid process type %s"%process_type)

        messages = ABDCPMessage.objects.filter(
            transaction_id= self.message.transaction_id,
            message_type= message_type
        )

        if len(messages)==0:
            raise Exception("We can't find %s message."%message_type)

        obj_messaje = self.processor_factory(messages[0])
        obj_messaje.load_number_information()

        operator = Operator.objects.get(code=obj_messaje.xmlmodel.codigo_receptor)

        if hasattr(obj_messaje.number_info,"error"):
            customer_name = "No existe en colca"
        else:
            customer_name = obj_messaje.number_info.customer.customer_name.encode('utf-8')

        number=obj_messaje.get_request_number().encode('utf-8')
        data = {
            "number":number,
            "customer_name": customer_name,
            "recipient": operator.name
        }

        if self.message.message_type=='PEP':
            data["detail"] = "Se comunica que se ha programado la fecha de portabilidad del cliente %s con número de teléfono %s , por favor proceder con la desafiliación administrativa y técnica en la fecha correspondiente." % (customer_name,number)
        elif self.message.message_type=='APDC':
            data["detail"] = "Se comunica que se ha acreditado la deuda del cliente %s con número de teléfono %s , por favor proceder con la desafiliación administrativa y técnica en la fecha correspondiente." % (customer_name,number)
        elif process_type == '05':
            data["detail"] = "Se comunica que el cliente %s ha relizado la consulta previa del número de teléfono %s ." %(customer_name,number)
        elif process_type == '01':
            data["detail"] = "Se comunica que el cliente %s ha solicitado la portabilidad del número de teléfono %s ." % (customer_name,number)

        return data

    def generate_data(self):
        data = self.get_deep_number_info()
        customer_name = data["customer_name"]
        number = data["number"]
        recipient = data["recipient"]
        customer_name = customer_name.decode('utf-8')
        number = number.decode('utf-8')

        message_type = getattr(strings,"ABDCP_MESSAGE_TYPE_%s"%self.__class__.__name__)
        data["subject"] = "%s del cliente %s" % (message_type,customer_name)
        data["process_name"] = message_type
        data["phone_number"] = number
        data["list_data"]={}
        data["list_data"]["Nombre/Razón Social"] = customer_name
        data["list_data"]["Teléfono"] = number
        data["list_data"]["Portador destino"] = recipient

        return data

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
