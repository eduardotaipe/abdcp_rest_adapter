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

        body  = "%s\n" % strings.ABDCP_MESSAGE_TYPE_SR
        
        body += "observaciones:%s\n" % xmlmodel.observaciones
        body += "codigo_receptor:%s\n" % xmlmodel.codigo_receptor
        body += "codigo_cedente:%s\n" % xmlmodel.codigo_cedente
        body += "numeracion_a_retornar:%s\n" % xmlmodel.numeracion_a_retornar
        body += "fecha_ejecucion_retorno:%s\n" % xmlmodel.fecha_ejecucion_retorno
        body += "motivo_retorno:%s\n" % xmlmodel.motivo_retorno
        body += "nombre_contacto:%s\n" % xmlmodel.nombre_contacto
        body += "email_contacto:%s\n" % xmlmodel.email_contacto
        body += "telefono_contacto:%s\n" % xmlmodel.telefono_contacto
        body += "fax_contacto:%s\n" % xmlmodel.fax_contacto

        info["body"] = body

        return info