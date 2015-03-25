# -*- coding: utf-8 -*-
from django.conf import settings

from abdcp_messages import strings
from abdcp_processes import ABDCP_Message
from abdcp_messages.xmlmodels import NE_ABDCP_XML_Message
from abdcp_messages.xmlmodels import NI_ABDCP_XML_Message

class NE(ABDCP_Message):

    xmlmodel_class = NE_ABDCP_XML_Message
    notify_to = settings.TELEPHONY_OPERATOR_EMAIL

    def generate_data(self):
        xmlmodel = self.xmlmodel
        data = {}
        data["subject"] = strings.ABDCP_MESSAGE_TYPE_NE
        data["phone_number"] = self.message.message_id
        data["process_name"] = strings.ABDCP_MESSAGE_TYPE_NE
        data["detail"] = ""

        data["list_data"]={}
        data["list_data"]["message_id"] = self.message.message_id
        data["list_data"]["codigo_error"] = \
            xmlmodel.codigo_error
        data["list_data"]["descripcion_codigo_error"] = \
            xmlmodel.descripcion_codigo_error

        return data

class NI(ABDCP_Message):

    xmlmodel_class = NI_ABDCP_XML_Message
    notify_to = settings.TELEPHONY_OPERATOR_EMAIL

    def generate_data(self):
        xmlmodel = self.xmlmodel
        data = {}
        data["subject"] ="No integridad %s" % xmlmodel.numero_secuencial_solicitud
        data["phone_number"] = self.message.message_id
        data["process_name"] = strings.ABDCP_MESSAGE_TYPE_NI
        data["detail"] = ""

        data["list_data"]={}
        data["list_data"]["message_id"] = self.message.message_id
        data["list_data"]["numero_secuencial_solicitud"] = \
            xmlmodel.numero_secuencial_solicitud
        data["list_data"]["identificador_mensaje_erroneo"] = \
            xmlmodel.identificador_mensaje_erroneo
        data["list_data"]["causa_no_integridad"] = \
            xmlmodel.causa_no_integridad
        data["list_data"]["fecha_recepcion_mensaje_anterior"] = \
            xmlmodel.get_last_message_reception_date_as_datetime()

        return data