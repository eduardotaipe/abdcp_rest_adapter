# -*- coding: utf-8 -*-

import time
from datetime import timedelta

from sequence_field.models import Sequence

from abdcp_adapter import settings
from abdcp_processes import ABDCP_Message
from abdcp_processes.tasks import process_message
from abdcp_messages import strings
from abdcp_messages import constants
from abdcp_messages.xmlbuilders import CPAC_XMLBuilder,CPOCC_XMLBuilder
from abdcp_messages.xmlmodels import ECPC_ABDCP_XML_Message, CPAC_ABDCP_XML_Message, CPOCC_ABDCP_XML_Message
from abdcp_messages.models import ABDCPMessage
from operators.models import Operator

############################
# Flujo de consulta previa #
############################
# RECIPIENT                             ABDCP                                 DONOR
#     +                                   +                                     +  
#     +--------------CP------------------->                                     |  
#     <-------------[NI]------------------+                                     |  
#     |                                   |                                     |  
#     <--------------ANCP-----------------+                                     |  
#     |                                   |                                     |  
#     <-------------[CPRABD]-------------------------------ECPC----------------->  
#     |                                   |                                     |  
#     |                                   |                                     |  
#     |                                   <---------------[CPOCC]---------------+  
#     <-------------[CPRABD]--------------+                                     |  
#     |                                   |                                     |  
#     |                                   |                                     |  
#     |                                   |                                     |  
#     |                                   <-----------------CPAC----------------+  
#     <--------------CPPR-----------------+                                     |  
#     |                                   |                                     |  
#     +                                   +                                     +  


class ANCP(ABDCP_Message):
    """asignacion de numero"""
    pass

class CPARBD(ABDCP_Message):
    """rechazo de consulta"""
    pass

class CPPR(ABDCP_Message):
    """Se concluye con exito la consulta previa"""
    pass

class CP(ABDCP_Message):
    """inicio de consulta previa"""
    def process(self):
        self.notify_ABDCP()
    
class CPOCC(ABDCP_Message):
    """respuesta de rechazo a la CP"""
    xmlmodel_class = CPOCC_ABDCP_XML_Message

    def generate_data(self):
        data = super(CPOCC, self).generate_data()
        number = data["number"]
        customer_name = data["customer_name"]
        reason = constants.OBJECTION_CAUSE[self.xmlmodel.causa_objecion]

        data["detail"]= "Se comunica el número %s del cliente %s ha sido consultado."% (number,customer_name)
        if "list_data" not in data:
            data["list_data"]={}
        data["list_data"]["Fecha y hora de consulta"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["list_data"]["Respuesta"] = "La consulta previa Fallida"
        data["list_data"]["Motivo de rechazo"] = reason
        return data

    def process(self):
        self.notify_ABDCP()
        self.notify()

class CPAC(ABDCP_Message):
    """respuesta ok de CP"""
    xmlmodel_class = CPAC_ABDCP_XML_Message

    def generate_data(self):
        data = super(CPAC, self).generate_data()
        number = data["number"]
        customer_name = data["customer_name"]

        data["detail"]= "Se comunica el número %s del cliente %s ha sido consultado."% (number,customer_name)
        if "list_data" not in data:
            data["list_data"]={}
        data["list_data"]["Fecha y hora de consulta"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["list_data"]["Respuesta"] = "La consulta exitosa"
        return data

    def process(self):
        self.notify_ABDCP()
        self.notify()


        
class ECPC(ABDCP_Message):
    """Consulta previa para el Cedente"""
    xmlmodel_class = ECPC_ABDCP_XML_Message

    def __init__(self, message):
        super(ECPC, self).__init__(message)
        self.set_api_client()


    def get_ABDCP_code(self):

        if self.query_number_has_errors():
            return constants.ABDCP_OC_SUSPEND_SERVICE
        
        if self.get_number_information() is None:
            return constants.ABDCP_OC_SUSPEND_SERVICE

        if self.phone_not_owned():
            return constants.ABDCP_OC_PHONE_NOT_OWNED

        if self.service_is_suspended():
            return constants.ABDCP_OC_SUSPEND_SERVICE

        if not self.valid_service_type():
            return constants.ABDCP_OC_INVALID_SERVICE_TYPE
        
        if not self.valid_portability_type():
            return constants.ABDCP_OC_INVALID_MODE

        if not self.valid_customer_id():
            return constants.ABDCP_OC_INVALID_ID_CUSTOMER

        if self.has_debt():
            return constants.ABDCP_OC_HAS_DEBT

        return "ok"

    def valid_portability_type(self):
        return self.get_query_mode_name() == self.get_request_portability_type()

    def has_debt(self):
        return self.get_query_debt_amount() is not None

    def valid_service_type(self):
        result = int(self.get_query_line_type()) == int(self.get_request_service_type())
        return result

    def valid_customer_id(self):
        num_info = self.get_number_information()
        if(num_info.customer is None):
            return False

        req_identity_number = self.get_request_identity_number()
        get_identity_number = self.get_query_identity_number()
        return req_identity_number == get_identity_number
    
    def phone_not_owned(self):
        number_info = self.get_number_information()
        if not hasattr(number_info, 'error'):
            return False
        return number_info.error.code == '1000'

    def service_is_suspended(self):
        service_status = self.get_query_service_status()
        return service_status == 'SUSPENDIDO'

    def get_query_debt_amount(self):
        num_info = self.get_number_information()
        if hasattr(num_info,'customer'):
            if hasattr(num_info.customer,'debt'):
                if hasattr(num_info.customer.debt,'amount'):
                    return num_info.customer.debt.amount
        return None

    def get_number_information(self):
        return getattr(self, 'number_info', None)

    def get_activation_date(self):
        return self.message.created + timedelta(days=1)

    def create_message(self):
        
        self.load_number_information()

        result = {
            'message_id' : self.generate_message_id(),
            'process_id' : self.xmlmodel.transaction_id,
            'sender_code' : settings.LOCAL_OPERATOR_ID,
            'recipient_code' : settings.ABDCP_OPERATOR_ID,
        }

        result_code = self.get_ABDCP_code()

        if result_code == "ok":
            result["numeracion"] = self.get_request_number()
            result["observaciones"] = strings.ABDCP_MESSAGE_PREVIOUS_CONSULT_ACCEPT
            result["fecha_activacion"] = self.get_activation_date()
            response = CPAC_XMLBuilder(**result)
            message_type = "CPAC"

        else:
            if result_code==constants.ABDCP_OC_HAS_DEBT:
                result["fecha_vencimiento"] = self.number_info.customer.debt.expiration_date
                result["monto"] = self.number_info.customer.debt.amount
                result["moneda"] = self.number_info.customer.debt.money_type

            result["causa_objecion"] = result_code
            result["numeracion"] = self.get_request_number()
            response = CPOCC_XMLBuilder(**result)
            message_type = "CPOCC"

        message = ABDCPMessage(
            message_id = result["message_id"],
            sender = Operator.objects.get(code=result["sender_code"]),
            recipient = Operator.objects.get(code=result["recipient_code"]),
            transaction_id = self.message.transaction_id,
            stated_creation = self.xmlmodel.get_message_creation_date_as_datetime(),
            message_type = message_type,
            process_type = '05',
            request_document = response.as_xml()
        )
        message.save()
        return message

        
    def get_request_number(self):
        return self.xmlmodel.numeracion

    def get_request_portability_type(self):
        if self.xmlmodel.tipo_portabilidad in constants.ABDCP_PORTABILITY_TYPE:
            return constants.ABDCP_PORTABILITY_TYPE[self.xmlmodel.tipo_portabilidad]
        return constants.ABDCP_PORTABILITY_TYPE['01']

    def load_number_information(self):        
        number = self.get_request_number()
        self.number_info = self.api.get_number(number)


    def query_number_has_errors(self):
        data = self.get_number_information()

        if hasattr(data,"error"):
            if hasattr(data.error,"code"):
                if int(data.error.code) in xrange(1000,1005):
                    return True

        return False

    def get_query_mode_name(self):
        num_info = self.get_number_information()
        mode_name = num_info.mode.mode_name
        return mode_name.upper()

    def get_query_service_status(self):
        num_info = self.get_number_information()
        return num_info.service_status

    def get_query_line_type(self):
        num_info = self.get_number_information()    
        return num_info.line_type.line_type_id

    def get_query_identity_number(self):
        num_info = self.get_number_information()
        return num_info.customer.customer_identity.identity_number

    def get_request_identity_number(self):
        return self.xmlmodel.numero_documento_identidad

    def get_request_service_type(self):
        return self.xmlmodel.tipo_servicio

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

    def process(self):
        message = self.create_message()
        process_message.delay(message.message_id)
        self.notify()
        