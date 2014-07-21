# -*- coding: utf-8 -*-
import datetime
import logging

from django.conf import settings

from requests_portability import PortabilityAPI
from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError

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
            return
        except ClientError,e:
            logging.error("set_api_cliente:client error")
        except APIError,e:
            logging.error("set_api_cliente:Api error")
        except AuthError,e:
            logging.error("Authentication error")
        self.api = None


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
        if self.response is not None:
            self.message.mark_responded(commit)


    def save_response(self, xmlstr=None):
        response = xmlstr if xmlstr is not None else self.response
        if response is not None:
            self.message.response_document = response
            self.message.save()


    def process_response(self, commit=True):
        response = self.generate_response()
        self.set_response(response)

    def process(self):
        self.process_response()
        self.save_response()
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

        


