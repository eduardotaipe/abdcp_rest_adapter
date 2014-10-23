# -*- coding: utf-8 -*-

import logging

from django.conf import settings

from abdcp_messages import strings
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ECPC_ABDCP_XML_Message
from abdcp_messages.xmlbuilders import CPAC_XMLBuilder,CPOCC_XMLBuilder
from abdcp_messages import constants
from abdcp_messages.tasks import send_message

from abdcp_processes import ABDCPProcessor

from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError

from sequence_field.models import Sequence

class ECPC_ABDCPProcessor(ABDCPProcessor):

    xmlmodel_class = ECPC_ABDCP_XML_Message

    def generate_message_id(self):
        message_type = self.message.message_type
        return Sequence.next(
            message_type + '_message',
            template='%(OO)s%Y%m%d%(TI)s%NNNNN', 
            params={
                'OO': settings.LOCAL_OPERATOR_ID,
                'TI': self.message.process_type
            }
        )

    def get_response_ok(self):
        common_data = self.get_header_data()
        common_data["numeracion"] = self.get_request_number()
        common_data["observaciones"] = strings.\
            ABDCP_MESSAGE_PREVIOUS_CONSULT_ACCEPT

        response = CPAC_XMLBuilder(**common_data)
        return response.as_xml()

    def get_response_error(self,error_code):
        common_data = self.get_header_data()
        common_data["causa_objecion"] = error_code
        common_data["numeracion"] = self.get_request_number()

        response = CPOCC_XMLBuilder(**common_data)
        return response.as_xml()

    def phone_not_owned(self):
        number_info = self.get_number_information()
        if not hasattr(number_info, 'error'):
            return False
        return number_info.error.code == '1000'

    def get_ABDCP_code(self):
        
        if self.get_number_information() is None:
            raise Exception("Fatal error: no number info")

        if self.phone_not_owned():
            return constants.ABDCP_OC_PHONE_NOT_OWNED

        if self.service_is_suspended():
            return constants.ABDCP_OC_SUSPEND_SERVICE

        if not self.valid_type_service():
            return constants.ABDCP_OC_INVALID_SERVICE_TYPE

        if not self.valid_customer_id():
            return constants.ABDCP_OC_INVALID_ID_CUSTOMER

        if self.has_debt():
            return constants.ABDCP_OC_HAS_DEBT

        return "ok"

    def generate_response(self):
        self.load_number_information()
        result_code = self.get_ABDCP_code()
        
        if result_code == "ok":
            return self.get_response_ok()

        return self.get_response_error(result_code)

    # Accessing request information

    def get_request_number(self):
        return self.xmlmodel.numeracion


    def get_request_line_type(self):
        return self.xmlmodel.tipo_portabilidad


    def get_request_identity_number(self):
        return self.xmlmodel.numero_documento_identidad

    
    def get_request_mode(self):
        return self.xmlmodel.tipo_servicio


    # Accesing number information

    def load_number_information(self):
        number = self.get_request_number()
        self.number_info = self.api.get_number(number)
    def get_number_information(self):
        return getattr(self, 'number_info', None)


    def get_query_number(self):
        num_info = self.get_number_information()
        return num_info.number


    def get_query_line_type(self):
        num_info = self.get_number_information()
        return num_info.line_type.line_type_id


    def get_query_identity_number(self):
        num_info = self.get_number_information()
        return num_info.customer.identity_number


    def get_query_identity_document_type(self):
        num_info = self.get_number_information()
        return num_info.customer.document_type


    def get_query_mode(self):
        num_info = self.get_number_information()
        return num_info.mode.mode_id


    def get_query_service_status(self):
        num_info = self.get_number_information()
        return num_info.service_status


    def service_is_suspended(self):
        service_status = self.get_query_service_status()
        return service_status == 'SUSPENDIDO'

    def valid_type_service(self):
        return self.get_query_line_type() == constants.LINE_TYPE_FIX
    
    def valid_customer_id(self):
        num_info = self.get_number_information()
        if(num_info.customer is None):
            return False

        req_identity_number = self.get_request_identity_number()
        get_identity_number = self.get_query_identity_number()
        return req_identity_number == get_identity_number


    def get_query_debt_amount(self):
        num_info = self.get_number_information()
        if hasattr(num_info,'customer'):
            if hasattr(num_info.customer,'debt'):
                if hasattr(num_info.customer.debt,'amount'):
                    return num_info.customer.debt.amount
        return None

    def has_debt(self):
        return self.get_query_debt_amount() is not None

    def process(self):
        self.process_response()
        self.save_response()
        self.mark_responded()
        send_message.delay(self.message.message_id)

