# -*- coding: utf-8 -*-

import time

from sequence_field.models import Sequence

from abdcp_adapter import settings
from abdcp_processes import ABDCP_Message
from abdcp_messages import strings
from abdcp_messages import constants
from abdcp_messages.xmlbuilders import CPAC_XMLBuilder,CPOCC_XMLBuilder
from abdcp_messages.xmlmodels import ECPC_ABDCP_XML_Message, CPAC_ABDCP_XML_Message, CPOCC_ABDCP_XML_Message
from abdcp_messages.models import ABDCPMessage
from operators.models import Operator
from abdcp_processes.tasks import process_message

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
        self.set_api_client()
        number = self.xmlmodel.numeracion.encode("utf-8")
        number_info = self.api.get_number(number)
        customer_name = number_info.customer.customer_name.encode('utf-8')
        
        data ={
            "subject":"Consulta Previa del cliente %s" % customer_name,
            "process_name":"CPOCC - %s" % strings.ABDCP_MESSAGE_TYPE_CPOCC,
            "phone_number":number,
        }

        data["detail"]= "Se comunica el número %s del cliente %s ha sido consultado."% (number,customer_name)
        data["list_data"]={}
        data["list_data"]["Nombre/Razon Social"] = customer_name
        data["list_data"]["Teléfono"] = number
        data["list_data"]["Fecha y hora de consulta"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["list_data"]["Portador destino"] = self.message.recipient.name
        data["list_data"]["Respuesta"] = "La consulta previa Fallida"
        data["list_data"]["Motivo de rechazo"] = constants.OBJECTION_CAUSE[self.xmlmodel.causa_objecion]
        
        return data

    def process(self):
        self.notify()
        self.notify_ABDCP()

class CPAC(ABDCP_Message):
    """respuesta ok de CP"""
    xmlmodel_class = CPAC_ABDCP_XML_Message

    def generate_data(self):
        self.set_api_client()
        number = self.xmlmodel.numeracion.encode("utf-8")
        number_info = self.api.get_number(number)
        customer_name = number_info.customer.customer_name.encode('utf-8')
        
        data ={
            "subject":"Consulta Previa del cliente %s" % customer_name,
            "process_name":"CPAC - %s" % strings.ABDCP_MESSAGE_TYPE_CPAC,
            "phone_number":number,
        }

        data["detail"]= "Se comunica el número %s del cliente %s ha sido consultado."% (number,customer_name)
        data["list_data"]={}
        data["list_data"]["Nombre/Razon Social"] = customer_name
        data["list_data"]["Teléfono"] = number
        data["list_data"]["Fecha y hora de consulta"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["list_data"]["Portador destino"] = self.message.recipient.name
        data["list_data"]["Respuesta"] = "La consulta previa exitosa"
        return data

    def process(self):
        self.notify()
        self.notify_ABDCP()


        
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

        if not self.valid_type_service():
            return constants.ABDCP_OC_INVALID_SERVICE_TYPE

        if not self.valid_customer_id():
            return constants.ABDCP_OC_INVALID_ID_CUSTOMER

        if self.has_debt():
            return constants.ABDCP_OC_HAS_DEBT

        return "ok"

    def has_debt(self):
        return self.get_query_debt_amount() is not None

    def valid_type_service(self):
        return self.get_query_line_type() == constants.LINE_TYPE_FIX

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
            response = CPAC_XMLBuilder(**result)
            message_type = "CPAC"

        else:
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

    def get_query_service_status(self):
        num_info = self.get_number_information()
        return num_info.service_status

    def get_query_line_type(self):
        num_info = self.get_number_information()
        return num_info.line_type.line_type_id

    def get_request_identity_number(self):
        return self.xmlmodel.numero_documento_identidad

    def get_query_identity_number(self):
        num_info = self.get_number_information()
        return num_info.customer.customer_identity.identity_number


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
        