# -*- coding: utf-8 -*-
from django.conf import settings

from abdcp_messages import strings
from abdcp_processes import Notifier_ABDCPProcessor
from abdcp_messages.xmlmodels import NE_ABDCP_XML_Message
from abdcp_messages.xmlmodels import NI_ABDCP_XML_Message

class NE_ABDCPProcessor(Notifier_ABDCPProcessor):

    xmlmodel_class = NE_ABDCP_XML_Message

    def get_email_info(self):
        xmlmodel = self.xmlmodel
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_NE
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone_number"] = "???"
        info["process_name"] = strings.ABDCP_MESSAGE_TYPE_NE
        info["list_data"]={}
        info["list_data"]["codigo_error"] = \
            xmlmodel.codigo_error
        info["list_data"]["descripcion_codigo_error"] = \
            xmlmodel.descripcion_codigo_error

        return info

class NI_ABDCPProcessor(Notifier_ABDCPProcessor):

    xmlmodel_class = NI_ABDCP_XML_Message

    def get_email_info(self):
        xmlmodel = self.xmlmodel
        info = {}
        info["subject"] = strings.ABDCP_MESSAGE_TYPE_NI
        info["to"] = settings.TELEPHONY_OPERATOR_EMAIL
        info["phone_number"] = "???"
        info["process_name"] = strings.ABDCP_MESSAGE_TYPE_NI

        info["list_data"]={}
        info["list_data"]["numero_secuencial_solicitud"] = \
            xmlmodel.numero_secuencial_solicitud
        info["list_data"]["identificador_mensaje_erroneo"] = \
            xmlmodel.identificador_mensaje_erroneo
        info["list_data"]["causa_no_integridad"] = \
            xmlmodel.causa_no_integridad
        info["list_data"]["fecha_recepcion_mensaje_anterior"] = \
            xmlmodel.get_last_message_reception_date_as_datetime()

        return info