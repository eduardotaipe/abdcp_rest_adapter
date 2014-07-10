# -*- coding: utf-8 -*-

from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import CP_ABDCP_XML_Message
from abdcp_processes import ABDCPProcessor

from requests_portability.client import PortabilityClientError as ClientError
from requests_portability.client import PortabilityAPIError as APIError
from requests_portability.client import PortabilityAuthError as AuthError


class CP_ABDCPProcessor(ABDCPProcessor):

    xmlmodel_class = CP_ABDCP_XML_Message


    def generate_response(self):
        op = self.load_number_information()


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
