# -*- coding: utf-8 -*-
import time

from abdcp_messages.models import ABDCPMessage
from abdcp_messages.xmlmodels import ESC_ABDCP_XML_Message, CPAC_ABDCP_XML_Message, CPOCC_ABDCP_XML_Message, CPSPR_ABDCP_XML_Message, SAC_ABDCP_XML_Message, PEP_ABDCP_XML_Message, OCC_ABDCP_XML_Message
from abdcp_messages import strings
from abdcp_messages import constants
from abdcp_messages.xmlbuilders import SAC_XMLBuilder,OCC_XMLBuilder

from abdcp_processes import ABDCP_Message
from abdcp_processes.cp import ECPC,CPAC
from abdcp_processes import settings
from abdcp_processes.tasks import process_message

from operators.models import Operator



class SP(ABDCP_Message):
    """Inicio Solicitud portabilidad"""
    pass

class ANS(ABDCP_Message):
    """Asignacion de numero"""
    pass
 
class RABDCP(ABDCP_Message):
    """Rejected SP by abdcp"""
    pass

class APDC(ABDCP_Message):
    """Acreditación pago deuda al cedente"""
    pass    

class SPR(ABDCP_Message):
    """Mensaje Final de Portacion exitosa"""
    def process(self):
        pass

class PEP(ABDCP_Message):
    """docstring for PEP"""
    xmlmodel_class = PEP_ABDCP_XML_Message

    def generate_data(self):
        
        data = super(PEP, self).generate_data()
        schedule_date = self.xmlmodel.get_scheduling_for_port_date_as_datetime()
        schedule_date = schedule_date.strftime("%Y-%m-%d %H:%M:%S")
        
        if "list_data" not in data:
            data["list_data"]={}
        data["list_data"]["Fecha y Hora de programación"] = schedule_date
        
        return data

class SAC(ABDCP_Message):
    """Aceptacion del cedente a la SP"""

    xmlmodel_class = SAC_ABDCP_XML_Message

    def process(self):
        self.notify()
        self.notify_ABDCP()
 
class OCC(ABDCP_Message):
    """Rechazo del cedente a la SP"""

    xmlmodel_class = OCC_ABDCP_XML_Message

    def generate_data(self):
        data = super(OCC, self).generate_data()
        number = data["number"]
        customer_name = data["customer_name"]
        reason = constants.OBJECTION_CAUSE[self.xmlmodel.causa_objecion]

        data["detail"]= "Se comunica el número %s del cliente %s ha sido consultado."% (number,customer_name)
        if "list_data" not in data:
            data["list_data"]={}
        data["list_data"]["Fecha y hora de consulta"] = time.strftime("%Y-%m-%d %H:%M:%S")
        data["list_data"]["Respuesta"] = "Solicitud de portabilidad Fallida"
        data["list_data"]["Motivo de rechazo"] = reason
        return data

    def process(self):
        self.notify()
        self.notify_ABDCP()



class CPSPR(ABDCP_Message):
    xmlmodel_class = CPSPR_ABDCP_XML_Message
    """Solicitud de portabilidad procedente por consulta previa procedente"""

    def get_acceptation_message(self):
        result = ABDCPMessage.objects.filter(
            transaction_id=self.xmlmodel.numero_consulta_previa,
            message_type= "CPAC"
        )

        if len(result)==0:
            raise Exception("We can't find CPAC message.")

        return CPAC(result[0])
    
    def generate_data(self):
        cpac = self.get_acceptation_message()
        data = cpac.generate_data()
        customer_name = data["list_data"]["Nombre/Razón Social"]
        number = data["list_data"]["Teléfono"]

        data["subject"] = "Solicitud de portabilidad del cliente %s" % customer_name
        data["process_name"] = '(CPSPR) Solicitud de portabilidad procedente por consulta previa procedente'
        data["detail"] = "Se comunica que el cliente %s ha solicitado la portabilidad del número de teléfono %s ." %(customer_name,number)
        data["list_data"]["Respuesta"] = "El teléfono %s ha sido portado" % number

        return data
        

class ESC(ECPC):
    xmlmodel_class = ESC_ABDCP_XML_Message

    """SP llega al cedente"""
    def process(self):
        message = self.create_message()
        process_message.delay(message.message_id)
        self.notify()

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
            response = SAC_XMLBuilder(**result)
            message_type = "SAC"

        else:
            if result_code==constants.ABDCP_OC_HAS_DEBT:
                result["fecha_vencimiento"] = self.number_info.customer.debt.expiration_date
                result["monto"] = self.number_info.customer.debt.amount
                result["moneda"] = self.number_info.customer.debt.money_type

            result["causa_objecion"] = result_code
            result["numeracion"] = self.get_request_number()
            response = OCC_XMLBuilder(**result)
            message_type = "OCC"

        message = ABDCPMessage(
            message_id = result["message_id"],
            sender = Operator.objects.get(code=result["sender_code"]),
            recipient = Operator.objects.get(code=result["recipient_code"]),
            transaction_id = self.message.transaction_id,
            stated_creation = self.xmlmodel.get_message_creation_date_as_datetime(),
            message_type = message_type,
            process_type = '01',
            request_document = response.as_xml()
        )
        message.save()
        return message
