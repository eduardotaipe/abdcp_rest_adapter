# -*- coding: utf-8 -*-

import logging
import json

from django.conf import settings

from abdcp_messages import strings
from abdcp_messages import constants
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ESC_ABDCP_XML_Message
from abdcp_messages.xmlmodels import PEP_ABDCP_XML_Message
from abdcp_messages.xmlmodels import SPR_ABDCP_XML_Message
from abdcp_messages.xmlbuilders import SAC_XMLBuilder,OCC_XMLBuilder

from abdcp_processes import ABDCPProcessor
from abdcp_processes import Notifier_ABDCPProcessor
from abdcp_processes.cp import ECPC_ABDCPProcessor

from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError

from sequence_field.models import Sequence

class ESC_ABDCPProcessor(ECPC_ABDCPProcessor):

    xmlmodel_class = ESC_ABDCP_XML_Message

    def process(self):
        self.process_response()
        self.save_response()
        self.mark_responded()

    def get_response_ok(self):
        common_data = self.get_header_data()
        common_data["observaciones"] = strings.\
            ABDCP_MESSAGE_PORT_REQUEST_ACCEPT

        response = SAC_XMLBuilder(**common_data)
        return response.as_xml()

    def get_response_error(self,error_code):
        common_data = self.get_header_data()
        common_data["causa_objecion"] = error_code
        common_data["numeracion"] = self.get_request_number()
        response = OCC_XMLBuilder(**common_data)
        return response.as_xml()


class PEP_ABDCPProcessor(Notifier_ABDCPProcessor):

    xmlmodel_class = PEP_ABDCP_XML_Message

    def get_email_info(self):
        esc = self.get_first_message_ESC()
        schedule_date=self.xmlmodel.get_scheduling_for_port_date_as_datetime()
        
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_PEP +": "+ esc.numeracion
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone_number"] = esc.numeracion
        info["process_name"] = strings.ABDCP_MESSAGE_TYPE_PEP
        
        info["list_data"]={}
        info["list_data"]["client_name"] = esc.nombre_contacto
        info["list_data"]["portablity_day"] = schedule_date
        info["body"] = body
        return info

class SPR_ABDCPProcessor(Notifier_ABDCPProcessor):

    xmlmodel_class = SPR_ABDCP_XML_Message

    def get_email_info(self):
        esc = self.get_first_message_ESC()
        fecha_limite_programacion_portabilidad= \
            self.xmlmodel.get_port_scheduling_limit_date_as_datetime()
        
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_SPR +": "+ esc.numeracion
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone_number"] = esc.numeracion
        info["process_name"] = strings.ABDCP_MESSAGE_TYPE_SPR

        info["list_data"]={}
        info["client_name"] = esc.nombre_contacto
        info["portablity_day"] = fecha_limite_programacion_portabilidad

        return info