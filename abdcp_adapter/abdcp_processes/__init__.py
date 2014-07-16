# -*- coding: utf-8 -*-

from django.conf import settings
from requests_portability import PortabilityAPI
from requests_portability.client import PortabilityClientError
from abdcp_adapter.utils import load_class
from abdcp_messages import constants

class ABDCPProcessor(object):

    def __init__(self, message=None):
        self.set_message(message)
        self.set_xmlmodel()
        self.set_response(None)
        self.set_api_client()


    def set_api_client(self):
        try:
            self.api = PortabilityAPI(
                base_url=settings.PORTABILITY_API_BASE_URL,
                api_key=settings.PORTABILITY_API_KEY
            )
            
        except PortabilityClientError,e:
            self.api = None
            logging.info("Error al Conectarse a ws-integracion-portabilidad")


    def set_message(self, message):
        self.message = message


    def set_response(self, xmlstr):
        self.response = xmlstr

    def set_xmlmodel(self):
        xmlstr = str(self.message.request_document)
        xmlmodel_class = self.get_xmlmodel_class()
        if xmlmodel_class is not None:
            self.xmlmodel = self.xmlmodel_class.create_from_string(xmlstr)
        else:
            self.xmlmodel = None


    def get_xmlmodel_class(self):
        return getattr(self, 'xmlmodel_class', None)


    def get_request_as_dict(self):
        return self.message.get_request_as_dict()


    def generate_response(self):
        pass


    def mark_responded(self, commit=True):
        self.message.mark_responded(commit)


    def save_response(self, xmlstr=None):
        response = xmlstr if xmlstr is not None else self.response
        if response is not None:
            self.message.response_document = response
            self.responded = datetime.datetime.now()
            self.save()


    def process_response(self, commit=True):
        response = self.generate_response()
        self.set_response(response)
        if response is not None and commit:
            self.save_response(response)

    def process(self):
        if self.api is None:
            logging.info("process: Error al Conectarse a "
                "ws-integracion-portabilidad")
            return False
        
        self.process_response()
        if self.response is not None:
            self.mark_responded()
        

    @classmethod
    def processor_factory(cls,message):
        process_type = \
            constants.ABDCP_PROCESS_CHOICES.get_key(message.process_type)
        message_type = message.message_type

        cls_path  = "abdcp_processes.%(process_type)s.%(message_type)s" 
        cls_path += "_ABDCPProcessor"
        cls_path  = cls_path % {
            "process_type" : process_type.lower(),
            "message_type" : message_type
        }

        try:
            klass = load_class(cls_path)
            return klass(message=message)
        except (ValueError,ImportError):
            return None

        


