# -*- coding: utf-8 -*-

from django.conf import settings
from abdcp_messages import strings
from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import CP_ABDCP_XML_Message
from abdcp_messages.xmlbuilders import CPAC_XMLBuilder,CPOCC_XMLBuilder
from abdcp_processes import ABDCPProcessor

from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError


class CP_ABDCPProcessor(ABDCPProcessor):

    xmlmodel_class = CP_ABDCP_XML_Message

    def get_common_data(self):
        #implementar sequence field
        import random
        result = {
            'message_id' : random.randint(0, 10000),
            'process_id' : random.randint(0, 10000),
            'sender_code' : settings.LOCAL_OPERADOR_ID,
            'recipient_code' : settings.ABDCP_OPERADOR_ID,
        }
        return result

    def get_response_ok_xml(self):
        common_data = self.get_common_data()
        common_data["numeracion"] = self.get_request_number()
        common_data["observaciones"] = strings.\
            ABDCP_MESSAGE_PREVIOUS_CONSULT_ACCEPT

        response = CPAC_XMLBuilder(**common_data)
        return response.as_xml()

    def get_response_error_xml(self):
        reason= "hmmmm"
        common_data = self.get_common_data()
        common_data["causa_objecion"] = reason
        common_data["numeracion"] = self.get_request_number()

        response = CPOCC_XMLBuilder(**common_data)
        return response.as_xml()

    def generate_response(self):
        if not self.load_number_information():
            return None
        
        if not self.check_number() or True:
            return self.get_response_error_xml()

        return self.get_response_ok_xml()

    # Accessing request information

    def get_request_number(self):
        return self.xmlmodel.inicio_rango


    def get_request_line_type(self):
        return self.xmlmodel.tipo_portabilidad


    def get_request_identity_number(self):
        return self.xmlmodel.numero_documento_identidad

    
    def get_request_mode(self):
        return self.xmlmodel.tipo_servicio


    # Accesing number information

    def load_number_information(self):
        number = self.get_request_number()
        try:
            self.number_info = self.api.get_number(number)
            return True
        except (ClientError, AuthError, APIError):
            self.number_info = None
            return False


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
        return num_info.customer.customer_identity.identity_number


    def get_query_identity_document_type(self):
        num_info = self.get_number_information()
        return num_info.customer.customer_identity.document_type


    def get_query_mode(self):
        num_info = self.get_number_information()
        return num_info.mode.mode_id


    def get_query_service_status(self):
        num_info = self.get_number_information()
        return num_info.service_status


    def service_is_suspended(self):
        service_status = self.get_query_service_status()
        return service_status == 'SUSPENDIDO'


    def get_query_debt_amount(self):
        num_info = self.get_number_information()
        if num_info.customer.debt is not None:
            return num_info.customer.debt.amount
        else:
            return None


    def has_debt(self):
        return self.get_query_debt_amount() is not None

    
    def check_number(self):
        requested_number = self.get_request_number()
        itp_number = self.get_query_number().replace('-','')
        return requested_number == itp_number

    def check_line_type(self):
        return "Se debe validar que el campo line_type tenga el valor Fijo."

    def check_number_owner(self):
        return "Se debe validar que el campo number este asociado al campo identity_number."

    def check_mode(self):
        return "Se debe validar que el campo mode tenga el valor PotsPago."
