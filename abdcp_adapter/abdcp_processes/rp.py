# -*- coding: utf-8 -*-
from django.conf import settings

from abdcp_messages import strings
from abdcp_processes import Notifier_ABDCPProcessor
from abdcp_messages.xmlmodels import SR_ABDCP_XML_Message

# solicitud de retorno
class SR_ABDCPProcessor(Notifier_ABDCPProcessor):

    xmlmodel_class = SR_ABDCP_XML_Message

    def get_email_info(self):
        xmlmodel = self.xmlmodel
        
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_SR +": " +\
            xmlmodel.numeracion_a_retornar
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone_number"] = xmlmodel.numeracion_a_retornar
        info["process_name"] = strings.ABDCP_MESSAGE_TYPE_SR

        info["list_data"] = {}
        info["list_data"]["observaciones"] = xmlmodel.observaciones
        info["list_data"]["codigo_receptor"] = xmlmodel.codigo_receptor
        info["list_data"]["codigo_cedente"] = xmlmodel.codigo_cedente
        info["list_data"]["numeracion_a_retornar"] = xmlmodel.numeracion_a_retornar
        info["list_data"]["fecha_ejecucion_retorno"] = xmlmodel.fecha_ejecucion_retorno
        info["list_data"]["motivo_retorno"] = xmlmodel.motivo_retorno
        info["list_data"]["nombre_contacto"] = xmlmodel.nombre_contacto
        info["list_data"]["email_contacto"] = xmlmodel.email_contacto
        info["list_data"]["telefono_contacto"] = xmlmodel.telefono_contacto
        info["list_data"]["fax_contacto"] = xmlmodel.fax_contacto

        return info