# -*- coding: utf-8 -*-

from django.conf import settings
from requests_portability import PortabilityAPI

class ABDCPProcessor(object):

    def __init__(self, message=None):
        self.set_message(message)
        self.set_xmlmodel()
        self.set_response(None)
        self.set_api_client()


    def set_api_client(self):
        self.api = PortabilityAPI(
            base_url=settings.PORTABILITY_API_BASE_URL,
            api_key=settings.PORTABILITY_API_KEY
        )


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
        if commit:
            self.save_response(response)


    def process(self):
        self.generate_response()
        self.save_response()
        self.mark_responded()
