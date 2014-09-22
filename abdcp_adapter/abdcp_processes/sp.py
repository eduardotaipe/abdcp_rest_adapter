# -*- coding: utf-8 -*-

import logging
import json

from django.conf import settings

from abdcp_messages import strings
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ESC_ABDCP_XML_Message
from abdcp_messages.xmlmodels import PEP_ABDCP_XML_Message
from abdcp_messages.xmlmodels import SPR_ABDCP_XML_Message
from abdcp_messages.xmlbuilders import SAC_XMLBuilder,OCC_XMLBuilder
from abdcp_messages import constants

from abdcp_processes import ABDCPProcessor
from abdcp_processes.cp import ECPC_ABDCPProcessor
from abdcp_processes.tasks import send_email

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

    def get_first_message_ESC(self):
        result = ABDCPMessage.objects.filter(
            transaction_id=self.message.transaction_id,
            message_type=constants.ABDCP_MESSAGE_TYPE_ESC
        )

        if result.count()==0:
            raise Exception("ESC message doesn't exist.")

        xmlstr = result[0].request_document
        esc = ESC_ABDCP_XML_Message.create_from_string(xmlstr)
        return esc


    def get_email_info(self):
        esc = self.get_first_message_ESC()
        schedule_date=self.xmlmodel.get_scheduling_for_port_date_as_datetime()
        
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_PEP +": "+ esc.numeracion
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone"] = esc.numeracion
        info["client_name"] = esc.nombre_contacto
        info["portablity_day"] = schedule_date

        body  = "cliente :%s\n" % info["client_name"]
        body += "telefono :%s\n" % info["phone"]
        body += "fecha :%s\n" % info["portablity_day"]
        info["body"] = body

        return info

    def notify(self):
        info = self.get_email_info()
        send_email.delay(info)

    def process(self):
        self.notify()


class SPR_ABDCPProcessor(PEP_ABDCPProcessor):

    xmlmodel_class = SPR_ABDCP_XML_Message

    def get_email_info(self):
        esc = self.get_first_message_ESC()
        schedule_date=self.xmlmodel.get_scheduling_for_port_date_as_datetime()
        
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_SPR +": "+ esc.numeracion
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone"] = esc.numeracion
        info["client_name"] = esc.nombre_contacto
        info["portablity_day"] = schedule_date

        body  = "cliente :%s\n" % info["client_name"]
        body += "telefono :%s\n" % info["phone"]
        body += "fecha :%s\n" % info["portablity_day"]
        info["body"] = body

        return info

