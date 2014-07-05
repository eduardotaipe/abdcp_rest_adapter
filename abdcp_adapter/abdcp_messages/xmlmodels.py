# -*- coding: utf-8 -*-

import datetime
from djxml import xmlmodels
from operators.models import Operator
from abdcp_messages.models import ABDCPMessage

class ABDCP_XML_Message(xmlmodels.XmlModel):

    message_id = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/IdentificadorMensaje'
    )

    sender = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/Remitente'
    )

    recipient = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/Destinatario'
    )

    message_creation_date = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/FechaCreacionMensaje'
    )

    transaction_id = xmlmodels.XPathTextField(
        '//MensajeABDCP/CabeceraMensaje/IdentificadorProceso'
    )

    message_type = xmlmodels.XPathTextField(
        '//MensajeABDCP/CuerpoMensaje/@IdMensaje'
    )

    def get_sender_as_operator(self):
        try:
            return Operator.objects.get(code=self.sender)
        except Operator.DoesNotExist:
            return None

    def get_recipient_as_operator(self):
        try:
            return Operator.objects.get(code=self.recipient)
        except Operator.DoesNotExist:
            return None

    def get_message_as_model(self):
        try:
            return ABDCPMessage.objects.get(message_id=self.message_id)
        except ABDCPMessage.DoesNotExist:
            return None

    def get_message_creation_date_as_datetime(self):
        src = self.message_creation_date
        return datetime.datetime.strptime(src,'%Y%m%d%H%M%S')
