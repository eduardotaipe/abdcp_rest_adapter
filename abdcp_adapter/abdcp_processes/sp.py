# -*- coding: utf-8 -*-

import logging
import json

from django.conf import settings

from abdcp_messages import strings
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ESC_ABDCP_XML_Message,PEP_ABDCP_XML_Message
from abdcp_messages.xmlbuilders import SAC_XMLBuilder,OCC_XMLBuilder
from abdcp_messages import constants

from abdcp_processes import ABDCPProcessor
from abdcp_processes.cp import ECPC_ABDCPProcessor

from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError

from sequence_field.models import Sequence


class ESC_ABDCPProcessor(ECPC_ABDCPProcessor):

    xmlmodel_class = ESC_ABDCP_XML_Message

    def get_response_ok(self):
        common_data = self.get_common_data()
        common_data["observaciones"] = strings.\
            ABDCP_MESSAGE_PORT_REQUEST_ACCEPT

        response = SAC_XMLBuilder(**common_data)
        return response.as_xml()

    def get_response_error(self,error_code):
        common_data = self.get_common_data()
        common_data["causa_objecion"] = error_code
        common_data["numeracion"] = self.get_request_number()

        response = OCC_XMLBuilder(**common_data)
        return response.as_xml()


class PEP_ABDCPProcessor(ABDCPProcessor):

    xmlmodel_class = PEP_ABDCP_XML_Message

    def generate_response(self):
        return "response PEP"

    def queue_notification(self):
        data_string = json.dumps(data)

    def process(self):
        super(PEP_ABDCPProcessor,self).process()
        self.queue_notification()

